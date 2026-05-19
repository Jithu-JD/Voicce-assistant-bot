# app/models/intent.py
from pydantic import BaseModel
from typing import Dict, List, Optional

class IntentResult(BaseModel):
    intent: str
    confidence: float
    entities: Dict[str, str] = {}
