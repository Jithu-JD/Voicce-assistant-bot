# Conversation model
# app/models/conversation.py
from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime

class Turn(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: Any
    ts: datetime

class Conversation(BaseModel):
    session_id: str
    user_id: str
    turns: List[Turn] = []
    summary: Optional[str] = None
