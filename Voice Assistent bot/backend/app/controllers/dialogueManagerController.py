# app/services/dialogue_manager.py
import json
from typing import List, Dict, Any
from flask import g

# Adjust these imports to match your layout
from .openaiServiceController import generate_text
from .knowledgeBaseController import search as kb_search
from .contextManagerController import last_k
from ..utils.timing import start_trace, span
from ..config import Settings

settings = Settings()

# -------- Tools ---------------------------------------------------------------

TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "kb_search",
            "description": "Search internal product & company KB.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    }
]

# -------- Helpers -------------------------------------------------------------

def _extract_text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    out = []
    try:
        for part in content or []:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    out.append(part.get("text", ""))
            else:
                if getattr(part, "type", None) == "text":
                    out.append(getattr(part, "text", ""))
    except Exception:
        pass
    return "".join(out).strip()

def _handle_tool_call(tool_name: str, arguments: dict):
    if tool_name == "kb_search":
        q = arguments.get("query", "") if isinstance(arguments, dict) else ""
        return {"results": kb_search(q, k=5)}
    return {"error": f"unknown tool {tool_name}"}

def _build_history(session_id: str, system_text: str, meta_text: str) -> List[Dict[str, str]]:
    history: List[Dict[str, str]] = [
        {"role": "system", "content": system_text},
        {"role": "system", "content": meta_text},
    ]
    for turn in last_k(session_id, 12):
        role = (turn.get("role") or "").lower()
        if role in ("user", "assistant"):
            history.append({"role": role, "content": str(turn.get("content", ""))})
    return history

# -------- Main ----------------------------------------------------------------

def generate_reply(session_id: str, system_text: str, meta_text: str, user_text: str) -> str:
    """
    Two-pass flow with timing:
      - PASS 1: Ask with tools enabled (tool_choice='auto')
      - PASS 2: If tools are called, fulfill and call again without tools
    """
    g.trace, log_trace = start_trace(f"generate_reply sid={session_id}")

    history: List[Dict[str, Any]] = _build_history(session_id, system_text, meta_text)
    history.append({"role": "user", "content": user_text})

    # ----- PASS 1 -------------------------------------------------------------
    with span("openai.pass1", g.trace):
        resp = generate_text(history, tools=TOOLS, tool_choice="auto")
    msg = resp.choices[0].message

    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls and len(tool_calls) > 0:
        # Append assistant with tool_calls
        assistant_msg: Dict[str, Any] = {
            "role": "assistant",
            "content": _extract_text(msg) or "",
            "tool_calls": []
        }
        for tc in tool_calls:
            assistant_msg["tool_calls"].append({
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
            })
        history.append(assistant_msg)

        # For each tool call, fulfill & time it
        for tc in tool_calls:
            with span(f"tool.{tc.function.name}", g.trace):
                try:
                    raw_args = tc.function.arguments
                    args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
                except Exception:
                    args = {}
                result = _handle_tool_call(tc.function.name, args)
            history.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, ensure_ascii=False)
            })

        # ----- PASS 2 ---------------------------------------------------------
        with span("openai.pass2", g.trace):
            resp2 = generate_text(history)  # no tools, no tool_choice
        log_trace()
        return _extract_text(resp2.choices[0].message)

    log_trace()
    return _extract_text(msg)
