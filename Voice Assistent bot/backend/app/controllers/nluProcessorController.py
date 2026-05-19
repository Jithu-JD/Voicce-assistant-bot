# app/services/nluProcessorController.py
import json
import re
from typing import Any, Dict, List
from flask import g

from .openaiServiceController import generate_text
from ..utils.timing import span
from ..config import Settings

settings = Settings()

def _to_string_messages(history_messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Ensure messages are in the Chat Completions string format:
      [{"role":"system|user|assistant","content":"..."}]
    If any message uses content-parts, join text parts into a single string.
    """
    out: List[Dict[str, str]] = []
    for m in history_messages or []:
        role = m.get("role") or "user"
        content = m.get("content", "")
        if isinstance(content, str):
            out.append({"role": role, "content": content})
        else:
            # try to join text parts
            text_bits = []
            try:
                for part in content or []:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_bits.append(part.get("text", ""))
                    elif hasattr(part, "type") and getattr(part, "type") == "text":
                        text_bits.append(getattr(part, "text", ""))
            except Exception:
                pass
            out.append({"role": role, "content": "".join(text_bits)})
    return out

def _json_from_text(s: str) -> Dict[str, Any]:
    """
    Best-effort JSON extraction:
      - try full parse
      - else extract first {...} block and parse
      - else return a safe default
    """
    try:
        return json.loads(s)
    except Exception:
        pass
    m = re.search(r"\{.*\}", s, flags=re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    # default shape to avoid caller crashes
    return {"intent": "unknown", "confidence": 0.0, "entities": {}}

def infer_intent_entities(history_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ask the model to return a compact JSON object:
      { "intent": string, "confidence": number (0..1), "entities": { k: v } }
    Adds timing so you can see how long NLU takes.
    """
    messages = _to_string_messages(history_messages)

    # Append a strict formatting instruction
    messages.append({
        "role": "system",
        "content": (
            "Extract intent and entities from the last user message.\n"
            "Return ONLY a compact JSON object with keys: intent (string), confidence (number 0..1), entities (object). "
            "Do not include any extra commentary."
        )
    })

    with span("nlu.infer", g.trace):
        resp = generate_text(
            messages,
            model=settings.DEFAULT_MODEL,
            temperature=0  # deterministic-ish, helps JSON reliability
        )

    # Chat Completions returns message.content as string
    msg = resp.choices[0].message
    text = msg.content if isinstance(msg.content, str) else ""
    data = _json_from_text(text)

    # Ensure required keys exist
    if "intent" not in data: data["intent"] = "unknown"
    if "confidence" not in data: data["confidence"] = 0.0
    if "entities" not in data or not isinstance(data["entities"], dict): data["entities"] = {}

    return data
