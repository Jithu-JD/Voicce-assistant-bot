# Speech recognition & synthesis
# app/controllers/speechServiceController.py
import io
from io import BytesIO
from openai import OpenAI
from ..config import Settings
from ..utils.timing import span

settings = Settings()
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    organization=settings.OPENAI_ORG,
    project=getattr(settings, "OPENAI_PROJECT", None)
)

# -------------------------
# STT (unchanged)
# -------------------------
def transcribe_audio(file_bytes: bytes, filename: str = "audio.wav"):
    with span("speech.stt"):
        file = io.BytesIO(file_bytes)
        file.name = filename
        tx = client.audio.transcriptions.create(
            model=settings.TRANSCRIBE_MODEL,
            file=file
        )
    return tx.text

# -------------------------
# Voice catalog (served to UI)
# -------------------------
# app/controllers/speechServiceController.py

SUPPORTED_VOICES = [
    {"id": "alloy",  "label": "Alloy (neutral)"},
    {"id": "ash",    "label": "Ash (deep)"},
    {"id": "coral",  "label": "Coral (bright)"},
    {"id": "echo",   "label": "Echo (balanced)"},
    {"id": "fable",  "label": "Fable (storyteller)"},
    {"id": "nova",   "label": "Nova (clear)"},
    {"id": "onyx",   "label": "Onyx (rich)"},
    {"id": "sage",   "label": "Sage (calm)"},
    {"id": "shimmer","label": "Shimmer (lively)"},
    
]
DEFAULT_VOICE = "shimmer"


def list_supported_voices() -> list[dict]:
    return SUPPORTED_VOICES

# NOTE: We no longer set an explicit output format.
# The streaming helper returns MP3 by default in current SDKs.
# TTS_OUTPUT_FORMAT kept here only for future use if needed.
TTS_OUTPUT_FORMAT = "mp3"  # (unused with streaming path)

# -------------------------
# TTS (Option A: streaming, no 'format' arg)
# -------------------------
def _tts_with_openai_streaming(text: str, voice: str) -> bytes:
    """
    Uses the streaming response helper to avoid passing 'format' or 'response_format'.
    Compatible across SDK versions that support `with_streaming_response`.
    """
    model = getattr(settings, "TTS_MODEL", None) or "gpt-4o-mini-tts"

    # Stream from API → memory (BytesIO)
    with span("speech.tts"):
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
        ) as resp:
            buf = BytesIO()
            for chunk in resp.iter_bytes():
                buf.write(chunk)
            return buf.getvalue()

def synthesize_tts(text: str, voice: str) -> bytes:
    voice = (voice or DEFAULT_VOICE).strip().lower()

    # Fallback if the requested voice isn’t in the catalog
    valid_voice_ids = {v["id"] for v in SUPPORTED_VOICES}
    if voice not in valid_voice_ids:
        voice = DEFAULT_VOICE

    audio_bytes = _tts_with_openai_streaming(text, voice)
    if not audio_bytes:
        raise RuntimeError("TTS returned empty audio")
    return audio_bytes
