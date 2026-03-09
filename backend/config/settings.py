from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "NeuralNotes"
    APP_NAME: str = "NeuralNotes"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    API_V1_STR: str = "/v1"
    SECRET_KEY: str = "your-secret-key-here"  # In production, use openssl rand -hex 32
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    # AI Settings
    WHISPER_MODEL: str = "base"
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Audio Settings
    MAX_AUDIO_FILE_SIZE_MB: int = 25
    AUDIO_TEMP_DIR: str = "temp_audio"

    # Firebase Settings

    FIREBASE_CREDENTIALS_PATH: Optional[str] = "./firebase_credentials.json"
    FIREBASE_PROJECT_ID: str = "neuralnotes-app"

    # Database
    REDIS_URL: str = "redis://localhost:6379"

    # Other
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()