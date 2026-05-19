# User model
# app/models/user.py
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: str
    name: Optional[str] = None
