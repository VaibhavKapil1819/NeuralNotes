# ============================================================
#  NeuralNotes — FastAPI Backend Entry Point
#  Run: uvicorn backend.main:app --reload --port 8000
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
from datetime import datetime
from backend.config.settings import settings
from backend.routes.meetings import router as meetings_router
from backend.routes.auth import router as auth_router


# ── Lifespan: runs on startup and shutdown ───────────────────
# WHY LIFESPAN?
# We want to load the Whisper model ONCE when the server starts,
# not on every request (model loading takes 5-10 seconds).
# Lifespan is FastAPI's modern way to run startup/shutdown logic.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ───────────────────────────────────────────────
    logger.info("🧠 NeuralNotes starting up...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Whisper model: {settings.WHISPER_MODEL}")

    # Initialize Firebase
    from backend.config.firebase import initialize_firebase
    initialize_firebase()

    # Pre-load Whisper model so first request is fast
    # from ai_pipeline.transcription.whisper_engine import whisper_engine
    # whisper_engine.load_model()

    logger.success("✅ NeuralNotes is ready!")
    yield   # App runs here

    # ── SHUTDOWN ──────────────────────────────────────────────
    logger.info("NeuralNotes shutting down...")


# ── App Initialization ───────────────────────────────────────
app = FastAPI(
    title="NeuralNotes API",
    description="AI Meeting Intelligence Platform — Turn every conversation into intelligence",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS Middleware ──────────────────────────────────────────
# Split allowed origins by comma if multiple are provided
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ─────────────────────────────────────────
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(meetings_router, prefix=settings.API_V1_STR)



# ── Health Check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "app":       settings.APP_NAME,
        "tagline":   "Turn every conversation into intelligence",
        "status":    "🟢 running",
        "version":   settings.APP_VERSION,
        "env":       settings.APP_ENV,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health", tags=["Health"])
def health_check():
    from ai_pipeline.transcription.whisper_engine import whisper_engine
    whisper_loaded = whisper_engine.model is not None

    return {
        "status": "healthy",
        "services": {
            "api":      "🟢 online",
            "whisper":  f"{'🟢 loaded' if whisper_loaded else '🔴 not loaded'} ({settings.WHISPER_MODEL})",
            "database": "🟡 not connected (Phase 3)",
            "claude":   "🟡 not connected (Phase 2)",
            "redis":    "🟡 not connected (Phase 5)",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }