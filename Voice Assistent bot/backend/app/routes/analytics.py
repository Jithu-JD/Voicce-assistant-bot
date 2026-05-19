# app/routes/analytics.py
from flask import Blueprint, jsonify
from ..database.mongo_client import db

bp = Blueprint("analytics", __name__)

@bp.get("/summary")
def summary():
    total = db["conversations"].count_documents({})
    return jsonify({"total_conversations": total})
