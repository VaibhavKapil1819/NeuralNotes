# ============================================================
#  NeuralNotes — Whisper Transcription Engine
#  Converts audio files to text using OpenAI Whisper
#
#  WHAT IS WHISPER?
#  A transformer-based Automatic Speech Recognition (ASR) model
#  trained on 680,000 hours of multilingual audio.
#  It runs completely locally — no API calls, no cost per minute.
# ============================================================

import whisper
import os
import time
from pydub import AudioSegment
from loguru import logger
from backend.config.settings import settings


class WhisperEngine:
    """
    Handles all audio transcription using OpenAI Whisper.

    WHY A CLASS?
    We load the Whisper model once when the app starts (it's large!).
    Then reuse the same loaded model for every transcription request.
    This avoids reloading the model on every request (would be very slow).
    """

    def __init__(self):
        self.model = None
        self.model_name = settings.WHISPER_MODEL  # reads from .env
        logger.info(f"WhisperEngine initialized. Model: {self.model_name}")

    def load_model(self):
        """
        Load the Whisper model into memory.
        Called once at app startup, not on every request.

        Model sizes and tradeoffs:
        tiny   → fastest, least accurate (~1GB RAM)
        base   → good balance for development (~1GB RAM)
        small  → better accuracy (~2GB RAM)
        medium → great accuracy (~5GB RAM)
        large  → best accuracy (~10GB RAM) — use in production
        """
        if self.model is None:
            logger.info(f"Loading Whisper model: '{self.model_name}'...")
            start = time.time()
            self.model = whisper.load_model(self.model_name)
            elapsed = round(time.time() - start, 2)
            logger.success(f"Whisper model loaded in {elapsed}s ✓")
        return self.model

    def convert_to_wav(self, input_path: str) -> str:
        """
        Convert any audio format to 16kHz mono WAV.
        Whisper works best with this specific format.

        WHY 16kHz MONO?
        Whisper was trained on 16kHz audio.
        Mono = single channel (removes stereo), reduces file size.
        """
        logger.info(f"Converting audio: {input_path}")

        # Create output path
        filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(settings.AUDIO_OUTPUT_DIR, f"{filename}_converted.wav")

        # Ensure output directory exists
        os.makedirs(settings.AUDIO_OUTPUT_DIR, exist_ok=True)

        # Load audio with pydub (handles MP3, MP4, WAV, M4A etc.)
        audio = AudioSegment.from_file(input_path)

        # Convert: stereo → mono, resample to 16kHz
        audio = audio.set_channels(1)       # mono
        audio = audio.set_frame_rate(16000) # 16kHz

        # Export as WAV
        audio.export(output_path, format="wav")
        logger.success(f"Audio converted → {output_path}")

        return output_path

    def transcribe(self, audio_path: str) -> dict:
        """
        Main transcription function.
        Takes an audio file path, returns structured transcript.

        Returns a dict with:
        - text: full transcript as a single string
        - segments: list of timed utterances
        - language: detected language code
        - duration: audio duration in seconds
        """
        logger.info(f"Starting transcription: {audio_path}")
        start_time = time.time()

        # Ensure model is loaded
        model = self.load_model()

        # Convert audio to Whisper-friendly format
        converted_path = self.convert_to_wav(audio_path)

        # Run Whisper transcription
        # verbose=False suppresses Whisper's own console output
        logger.info("Running Whisper inference...")
        result = model.transcribe(
            converted_path,
            verbose=False,
            task="transcribe",       # transcribe = keep original language
                                     # translate  = force translate to English
        )

        elapsed = round(time.time() - start_time, 2)
        logger.success(f"Transcription complete in {elapsed}s ✓")

        # Clean up converted file
        if os.path.exists(converted_path):
            os.remove(converted_path)

        # Format segments into clean utterances
        utterances = []
        for segment in result.get("segments", []):
            utterances.append({
                "id":         segment["id"],
                "text":       segment["text"].strip(),
                "start_time": round(segment["start"], 2),
                "end_time":   round(segment["end"], 2),
                "speaker":    "Speaker 1",   # diarization added in Phase 2
            })

        return {
            "full_text":          result["text"].strip(),
            "utterances":         utterances,
            "language":           result.get("language", "en"),
            "duration_seconds":   utterances[-1]["end_time"] if utterances else 0,
            "word_count":         len(result["text"].split()),
            "processing_time_s":  elapsed,
            "model_used":         self.model_name,
        }

    def cleanup(self, file_path: str):
        """Delete a temp file after processing."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not delete temp file {file_path}: {e}")


# ── Single instance reused across all requests ───────────────
# WHY GLOBAL INSTANCE?
# Whisper model is large — we load it once at startup.
# Every API request uses this same loaded instance.
whisper_engine = WhisperEngine()