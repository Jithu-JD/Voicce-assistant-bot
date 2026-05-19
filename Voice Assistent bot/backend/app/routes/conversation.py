# app/routes/conversation.py

from flask import Blueprint, request, jsonify
from ..controllers.conversationManagerController import converse
from ..models.prompt_envelope import PromptEnvelope  # import Pydantic model with DB access
bp = Blueprint("conversation", __name__)

@bp.post("/chat")
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_text = data.get("text")

    if not session_id or not user_text:
        return jsonify({"ok": False, "error": "Missing session_id or text"}), 400

    # 🔍 Fetch prompt envelope from MongoDB via model
    prompt_env_model = PromptEnvelope.get_by_session(session_id)
    if not prompt_env_model:
        return jsonify({"ok": False, "error": f"No prompt envelope found for session {session_id}"}), 404

    # 🧠 Convert to dict to pass downstream
    prompt_env = prompt_env_model.dict()
    print("prompt_env:---")
    print(prompt_env)

    reply = converse(session_id, prompt_env, user_text)
    return jsonify({"ok": True, "reply": reply})


@bp.post("/robot_chat")
def robot_chat():
    data = request.get_json()
    face = data.get("face")
    user_text = data.get("text")

    if not face or not user_text:
        return jsonify({"ok": False, "error": "Missing face or text"}), 400

    # ✅ TEMP: Just log face
    print(f"[ROBOT CHAT] Face detected: {face}")

    # ✅ Use fixed session_id for now
    session_id = "demo-session-1"

    from ..models.prompt_envelope import PromptEnvelope
    from ..controllers.conversationManagerController import converse

    prompt_env_model = PromptEnvelope.get_by_session(session_id)
    if not prompt_env_model:
        return jsonify({"ok": False, "error": "Prompt envelope not found for default session"}), 404

    prompt_env = prompt_env_model.dict()
    reply = converse(session_id, prompt_env, user_text)
    return jsonify({"ok": True, "reply": reply})
