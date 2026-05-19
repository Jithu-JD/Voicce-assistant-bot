# app/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_ORG: str | None = None
    MONGO_URI: str | None = None
    REDIS_URL: str = "redis://localhost:6379/0"
    CORS_ORIGINS: str = "*"
    DEFAULT_MODEL: str = "gpt-5"            # pick your main text model
    TRANSCRIBE_MODEL: str = "gpt-4o-transcribe"  # STT
    TTS_MODEL: str = "tts-1"               # TTS voice model
    EMBEDDING_MODEL: str = "text-embedding-3-large"
    REALTIME_MODEL: str = "gpt-4o-realtime-preview"  # WebRTC/WebSocket
    BRAND_PERSONA_FILE: str = "app/templates/prompts/base_persona.txt"

    class Config:
        env_file = ".env"
