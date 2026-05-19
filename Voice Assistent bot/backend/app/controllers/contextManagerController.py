# app/services/contextManagerController.py
from ..database.mongo_client import db
from datetime import datetime
from ..utils.timing import span

convos = db["conversations"]

def append_turn(session_id: str, role: str, content):
    with span("context.append_turn"):
        convos.update_one(
            {"_id": session_id},
            {"$push": {"turns": {"role": role, "content": content, "ts": datetime.utcnow()}}},
            upsert=True
        )

def last_k(session_id: str, k=12):
    with span("context.last_k"):
        doc = convos.find_one({"_id": session_id}) or {}
        return (doc.get("turns") or [])[-k:]

def set_summary(session_id: str, summary: str):
    with span("context.set_summary"):
        convos.update_one(
            {"_id": session_id},
            {"$set": {"summary": summary}},
            upsert=True
        )
