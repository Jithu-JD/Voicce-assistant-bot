# Authentication routes

# app/routes/auth.py
from flask import Blueprint, jsonify
from ..config import Settings
from openai import OpenAI
bp = Blueprint("auth", __name__)
settings = Settings()

@bp.get("/realtime-ephemeral")
def get_ephemeral_token():
    """
    The browser will use this token to open a WebRTC session with OpenAI Realtime.
    Ref: Realtime WebRTC flow. :contentReference[oaicite:8]{index=8}
    """
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    # Python SDK exposes a Session token creation; if not, POST to REST directly.
    # Pseudo (adapt if SDK differs):
    resp = client.realtime.sessions.create(model=settings.REALTIME_MODEL)
    return jsonify(resp)
