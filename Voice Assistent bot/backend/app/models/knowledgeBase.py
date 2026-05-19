# Knowledge base model

# app/models/knowledge_base.py
from pydantic import BaseModel
from typing import List

class KBChunk(BaseModel):
    id: str
    text: str
    embedding: List[float]
    meta: dict = {}
