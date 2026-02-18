# ============================================================
#  NeuralNotes — Meetings API Routes
#  Handles audio upload and transcription (Phase 1)
# ============================================================

import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from datetime import datetime
from backend.config.settings import settings
from ai_pipeline.transcription.whisper_engine import whisper_engine

# ── Router ───────────────────────────────────────────────────
# A router groups related endpoints together.
# This router handles everything under /v1/meetings/
router = APIRouter(prefix="/v1/meetings", tags=["Meetings"])

# ── Allowed audio formats ────────────────────────────────────
ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".webm", ".flac"}
MAX_FILE_SIZE_BYTES = settings.MAX_AUDIO_FILE_SIZE_MB * 1024 * 1024


# ── Helper: validate uploaded file ───────────────────────────
def validate_audio_file(file: UploadFile):
    """Check file extension and content type before processing."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {ALLOWED_EXTENSIONS}"
        )


# ── Helper: save upload to temp folder ───────────────────────
def save_upload(file: UploadFile) -> str:
    """Save uploaded file to temp directory. Returns file path."""
    os.makedirs(settings.AUDIO_TEMP_DIR, exist_ok=True)

    # Generate unique filename to avoid collisions
    ext = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.AUDIO_TEMP_DIR, unique_name)

    # Write file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    logger.info(f"Saved upload: {file_path} ({file_size_mb} MB)")

    return file_path


# ── POST /v1/meetings/upload ──────────────────────────────────
@router.post("/upload")
async def upload_meeting(
    file: UploadFile = File(..., description="Audio or video file of the meeting"),
    title: str = Form(default="Untitled Meeting"),
    participants: str = Form(default=""),
    language: str = Form(default="auto"),
):
    """
    Upload a meeting audio file and get a transcript back.

    This is Phase 1 — pure transcription, no AI analysis yet.
    Phase 2 will add: summary, action items, speaker labels.

    Steps:
    1. Validate file type
    2. Save to temp directory
    3. Convert to WAV via ffmpeg
    4. Run Whisper transcription
    5. Return structured transcript
    6. Cleanup temp files
    """
    logger.info(f"Upload received: '{file.filename}' | Title: '{title}'")

    # ── Step 1: Validate ─────────────────────────────────────
    validate_audio_file(file)

    # ── Step 2: Save to disk ──────────────────────────────────
    temp_path = save_upload(file)

    try:
        # ── Step 3 & 4: Transcribe (convert + run Whisper) ────
        logger.info("Sending to Whisper engine...")
        transcript = whisper_engine.transcribe(temp_path)

        # ── Step 5: Build response ────────────────────────────
        meeting_id = f"mtg_{uuid.uuid4().hex[:8]}"

        response = {
            "status":     "success",
            "meeting_id": meeting_id,
            "title":      title,
            "filename":   file.filename,
            "uploaded_at": datetime.utcnow().isoformat(),
            "transcript": {
                "full_text":         transcript["full_text"],
                "utterances":        transcript["utterances"],
                "language":          transcript["language"],
                "duration_seconds":  transcript["duration_seconds"],
                "word_count":        transcript["word_count"],
            },
            "processing": {
                "model_used":          transcript["model_used"],
                "processing_time_s":   transcript["processing_time_s"],
            },
            "next_steps": "Phase 2 will add: summary, action items, speaker labels",
        }

        logger.success(f"Transcription complete for meeting: {meeting_id}")
        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    finally:
        # ── Step 6: Always clean up temp file ─────────────────
        # 'finally' runs whether success or error
        whisper_engine.cleanup(temp_path)


# ── GET /v1/meetings ──────────────────────────────────────────
@router.get("/")
def list_meetings():
    """
    List all meetings.
    Phase 1: returns mock data.
    Phase 3: will return real data from Firebase Firestore.
    """
    return {
        "status": "success",
        "meetings": [],
        "note": "Firebase integration coming in Phase 3"
    }


# ── GET /v1/meetings/{meeting_id} ─────────────────────────────
@router.get("/{meeting_id}")
def get_meeting(meeting_id: str):
    """
    Get a single meeting by ID.
    Phase 1: returns mock.
    Phase 3: will fetch from Firestore.
    """
    return {
        "status": "success",
        "meeting_id": meeting_id,
        "note": "Firebase integration coming in Phase 3"
    }