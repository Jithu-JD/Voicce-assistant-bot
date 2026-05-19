# Knowledge base operations
# app/services/knowledge_service.py
from ..config import Settings
from .openaiServiceController import client
from ..database.mongo_client import db
from ..utils.timing import span
import numpy as np

settings = Settings()
kb_col = db["kb"]
emb_col = db["kb_embeddings"]

def embed(texts: list[str]) -> list[list[float]]:
    with span("kb.embed"):
        res = client.embeddings.create(model=settings.EMBEDDING_MODEL, input=texts)
        return [d.embedding for d in res.data]

def upsert_document(doc_id: str, text: str, meta: dict):
    with span("kb.upsert"):
        vec = embed([text])[0]
        emb_col.update_one(
            {"_id": doc_id},
            {"$set": {"embedding": vec, "meta": meta, "text": text}},
            upsert=True
        )

def search(query: str, k=5):
    with span("kb.search"):
        qv = np.array(embed([query])[0])
        # naive cosine search; replace with Atlas Vector, pgvector, or Redis Search in prod
        rows = list(emb_col.find({}, {"embedding": 1, "text": 1, "meta": 1}))
        scored = []
        for r in rows:
            v = np.array(r["embedding"])
            score = float(qv @ v / (np.linalg.norm(qv) * np.linalg.norm(v) + 1e-9))
            scored.append((score, r))
        scored.sort(reverse=True, key=lambda x: x[0])
        return [{"score": s, "text": r["text"], "meta": r["meta"]} for s, r in scored[:k]]
