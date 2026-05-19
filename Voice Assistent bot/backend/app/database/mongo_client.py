# app/database/mongo_client.py
from pymongo import MongoClient
from ..config import Settings

settings = Settings()
mongo = MongoClient(settings.MONGO_URI)
db = mongo["delegate_bot"]
