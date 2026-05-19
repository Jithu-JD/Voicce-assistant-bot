# app/models/prompt_envelope.py

from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.database.mongo_client import db


class FADetail(BaseModel):
    name: str
    role: str
    likes: str
    dislikes: str
    dob:str

class PromptEnvelope(BaseModel):
    session_id: str
    myName: str
    myRole: str
    fa: str
    sa: str
    ta: str
    faDetail: FADetail
    relationWithFA: str
    timeDate: str
    contextPlaceEvent: str
    contextRole: str
    emotion: str
    goalOfConversation: str
    caution: str
    ReferenceSourceForProductAndCompany: str
    ConversationStyle: str
    ConversaionPhase: Optional[str] = None
    Instruction: str

    @classmethod
    def get_by_session(cls, session_id: str) -> Optional["PromptEnvelope"]:
        data = db.prompt_envelope.find_one({"session_id": session_id}, {"_id": 0})
        if data:
            return cls(**data)
        return None
