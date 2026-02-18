# ============================================================
#  NeuralNotes — App Settings
#  Reads all environment variables from .env file
#  Every other file imports settings from here
#  Never read os.environ directly anywhere else!
# ============================================================

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    All app configuration lives here.
    Values are automatically read from your .env file.
    If a value is missing from .env, the default is used.
    """

    # ── App ───────────────────────────────────────────────────
    APP_NAME: str = "NeuralNotes"
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ── API ───────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production"
    ALLOWED_ORIGINS: str = "http://localhost:8501"

    # ── AI Services ───────────────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    WHISPER_MODEL: str = "base"        # tiny | base | small | medium | large-v3
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS: int = 4096

    # ── Firebase ──────────────────────────────────────────────
    FIREBASE_CREDENTIALS_PATH: str = "./firebase_credentials.json"
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""

    # ── Email ─────────────────────────────────────────────────
    SENDGRID_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@neuralnotes.ai"
    EMAIL_FROM_NAME: str = "NeuralNotes"

    # ── Redis ─────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379"

    # ── Audio ─────────────────────────────────────────────────
    MAX_AUDIO_FILE_SIZE_MB: int = 500
    AUDIO_CHUNK_DURATION_MINUTES: int = 30
    AUDIO_TEMP_DIR: str = "./temp/audio"
    AUDIO_OUTPUT_DIR: str = "./temp/processed"

    # ── ChromaDB ──────────────────────────────────────────────
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "neuralnotes_meetings"

    # ── Logging ───────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"              # reads from .env automatically
        env_file_encoding = "utf-8"
        extra = "ignore"               # ignore unknown variables in .env


@lru_cache()                           # cache so .env is only read once
def get_settings() -> Settings:
    return Settings()


# ── Single instance used everywhere ─────────────────────────
settings = get_settings()