# Knowledge base routes

# app/routes/knowledge.py
from flask import Blueprint, request, jsonify
from ..controllers.knowledgeBaseController import upsert_document, search

bp = Blueprint("knowledge", __name__)

@bp.post("/upsert")
def upsert():
    payload = request.get_json()
    upsert_document(payload["id"], payload["text"], payload.get("meta", {}))
    return jsonify({"ok": True})

@bp.get("/search")
def kbsearch():
    q = request.args.get("q")
    k = int(request.args.get("k", "5"))
    return jsonify({"ok": True, "hits": search(q, k=k)})
