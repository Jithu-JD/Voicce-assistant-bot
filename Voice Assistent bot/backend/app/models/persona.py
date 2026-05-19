# app/models/persona.py
from pydantic import BaseModel

class Persona(BaseModel):
    name: str = "AIRA"
    description: str = "Executive-grade delegate; witty, concise, persuasive."
    style: str = "Short lines. Anchor-like turn-taking. Business tone."
