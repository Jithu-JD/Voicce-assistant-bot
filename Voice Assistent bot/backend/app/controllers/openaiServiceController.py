# app/controllers/openaiServiceController.py
from openai import OpenAI
from flask import g
from ..config import Settings
from ..utils.timing import span
import logging

settings = Settings()
log = logging.getLogger(__name__)

# Optional: set a client timeout to fail fast on slow networks (tune as needed)
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    organization=settings.OPENAI_ORG,
    project=getattr(settings, "OPENAI_PROJECT", None),
    timeout=15.0  # seconds
)

def generate_text(messages, tools=None, tool_choice=None, model=None, stream=False, **extra):
    """
    messages: [{"role":"system/user/assistant","content":"..."}]
    tools: OpenAI tools (function calling). Only set tool_choice when tools are provided.
    stream: if True, returns a streaming iterator (timed as a single span)
    extra: pass-through for params like temperature, max_tokens, etc.
    """
    #model = model or settings.DEFAULT_MODEL
    model = 'gpt-4o-mini'
    params = {"model": model, "messages": messages, **extra}

    if tools:
        params["tools"] = tools
        if tool_choice:
            params["tool_choice"] = tool_choice
    # (No tool_choice when tools is None — avoids 400)

    label = f"openai.chat [{model}]"
    trace_ctx = getattr(g, "trace", None)

    if stream:
        with span(label, trace_ctx):
            return client.chat.completions.create(stream=True, **params)
    else:
        with span(label, trace_ctx):
            resp = client.chat.completions.create(**params)

        # 🔎 Usage logging (prompt/completion/total tokens)
        try:
            u = resp.usage
            msg = f"[USAGE] model={model} prompt={u.prompt_tokens} completion={u.completion_tokens} total={u.total_tokens}"
            log.info(msg)
            print(msg)  # visible in console even without logging config
        except Exception:
            pass

        return resp