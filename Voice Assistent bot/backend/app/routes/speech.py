# app/routes/speech.py  (Speech processing routes)

from flask import Blueprint, request, send_file, jsonify
from ..controllers.speechServiceController import transcribe_audio, synthesize_tts
from io import BytesIO
import time

bp = Blueprint("speech", __name__)

def _sniff_audio_mime(b: bytes) -> tuple[str, str]:
    # crude but effective type/extension detection
    if len(b) >= 12 and b[:4] == b"RIFF" and b[8:12] == b"WAVE":
        return "audio/wav", "wav"
    if len(b) >= 3 and b[:3] == b"ID3":
        return "audio/mpeg", "mp3"
    if len(b) >= 2 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0:
        return "audio/mpeg", "mp3"
    if len(b) >= 4 and b[:4] == b"OggS":
        return "audio/ogg", "ogg"
    return "application/octet-stream", "bin"

@bp.post("/stt")
def stt():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "no file"}), 400
    f = request.files["file"]
    try:
        t0 = time.perf_counter()
        text = transcribe_audio(f.read(), filename=f.filename)
        ms = int((time.perf_counter() - t0) * 1000)
        return jsonify({"ok": True, "text": text, "stt_ms": ms})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502

@bp.post("/tts")
def tts():
    data = request.get_json(force=True, silent=False)
    text = (data.get("text") or "").strip()
    voice = (data.get("voice") or "verse").strip().lower()
    download = bool(request.args.get("download"))  # ?download=1

    if not text:
        return jsonify({"ok": False, "error": "text required"}), 400

    try:
        t0 = time.perf_counter()
        audio_bytes = synthesize_tts(text, voice=voice)
        ms = int((time.perf_counter() - t0) * 1000)

        mime, ext = _sniff_audio_mime(audio_bytes)
        buf = BytesIO(audio_bytes)
        resp = send_file(
            buf,
            mimetype=mime,
            as_attachment=download,
            download_name=f"aira.{ext}"
        )
        resp.headers["X-TTS-Ms"] = str(ms)
        resp.headers["Content-Length"] = str(len(audio_bytes))
        resp.headers["Cache-Control"] = "no-store"
        return resp
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502
    
@bp.get("/voices")
def voices():
    try:
        from ..controllers.speechServiceController import list_supported_voices
        return jsonify({"ok": True, "voices": list_supported_voices()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 502
