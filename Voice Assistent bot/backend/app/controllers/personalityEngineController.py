# app/services/personalityEngineController.py
from ..config import Settings

def load_persona_system_prompt():
    with open(Settings().BRAND_PERSONA_FILE, "r", encoding="utf-8") as f:
        return f.read()

def make_context_block(prompt_envelope: dict, fa_prompt: str):
    # Convert your provided Prompt Generation array → a compact system/user framing
    # Keep lines short, witty (your constraint)
    sys = load_persona_system_prompt()
    sys += "\n\n[Brand Voice] Short, witty lines. Executive presence. No rambling."
    sys += "\n[Turn-taking] Keep answers crisp; invite brief replies."
    sys += "\n[Escalation] Offer handoff when confidence low or stakes high."
    meta = f"[Context] {prompt_envelope}"
    usr = f"FAPrompt: {fa_prompt}"
    return sys, meta, usr
