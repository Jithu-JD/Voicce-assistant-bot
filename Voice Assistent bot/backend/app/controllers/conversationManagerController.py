
from flask import g
from ..utils.timing import span

from .personalityEngineController import make_context_block
from .contextManagerController import append_turn
from .dialogueManagerController import generate_reply
from .personalityEngineController import make_context_block

def converse(session_id: str, prompt_env: dict, user_text: str) -> str:
    # Build the system/meta/user blocks from persona + envelope
    system_text, meta_text, user_text_fmt = make_context_block(prompt_env, user_text)

    # (optional) store the incoming user turn
    append_turn(session_id, role="user", content=user_text)

    # Generate the assistant’s reply (dialogue manager may do KB, tools, etc.)
    reply = generate_reply(session_id, system_text, meta_text, user_text_fmt)

    # (optional) store the assistant turn
    append_turn(session_id, role="assistant", content=reply)

    return reply