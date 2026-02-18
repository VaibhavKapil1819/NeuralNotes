# ============================================================
#  NeuralNotes — FastAPI Backend Entry Point
#  Run: uvicorn backend.main:app --reload --port 8000
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# ── App Initialization ───────────────────────────────────────
app = FastAPI(
    title="NeuralNotes API",
    description="AI Meeting Intelligence Platform — Turn every conversation into intelligence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ──────────────────────────────────────────
# Allows the Streamlit frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "app": "NeuralNotes",
        "tagline": "Turn every conversation into intelligence",
        "status": "🟢 running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "services": {
            "api":       "🟢 online",
            "database":  "🟡 not connected (mock mode)",
            "whisper":   "🟡 not loaded (mock mode)",
            "claude":    "🟡 not connected (mock mode)",
            "redis":     "🟡 not connected (mock mode)",
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


# ── Mock Auth Endpoints ──────────────────────────────────────
@app.post("/v1/auth/register", tags=["Auth"])
def mock_register():
    return {
        "status": "success",
        "message": "✅ Mock user registered (Firebase not connected yet)",
        "user": {
            "id": "mock_user_001",
            "email": "naveen@neuralnotes.ai",
            "display_name": "Naveen",
            "org_id": "mock_org_001",
            "role": "admin",
        }
    }


@app.post("/v1/auth/login", tags=["Auth"])
def mock_login():
    return {
        "status": "success",
        "message": "✅ Mock login successful (Firebase not connected yet)",
        "id_token": "mock_jwt_token_xxxxx",
        "expires_in": 3600,
        "user": {
            "id": "mock_user_001",
            "email": "naveen@neuralnotes.ai",
            "display_name": "Naveen",
            "role": "admin",
        }
    }


@app.get("/v1/auth/me", tags=["Auth"])
def mock_me():
    return {
        "id": "mock_user_001",
        "email": "naveen@neuralnotes.ai",
        "display_name": "Naveen",
        "role": "admin",
        "org_id": "mock_org_001",
        "org_name": "NeuralNotes Dev",
    }


# ── Mock Meeting Endpoints ───────────────────────────────────
MOCK_MEETINGS = [
    {
        "id": "mtg_001",
        "title": "Q3 Planning Session",
        "date": "2026-02-18T10:00:00Z",
        "duration": "45 mins",
        "participants": ["naveen@neuralnotes.ai", "alice@company.com"],
        "status": "completed",
        "tags": ["planning", "q3", "budget"],
        "summary": "The team aligned on Q3 priorities. Budget was approved. Product launch moved to Q4.",
        "action_items": [
            {"task": "Send budget proposal to finance", "assignee": "Naveen", "due": "2026-02-25"},
            {"task": "Update product roadmap", "assignee": "Alice", "due": "2026-02-22"},
        ],
        "sentiment": "positive",
    },
    {
        "id": "mtg_002",
        "title": "Engineering Standup",
        "date": "2026-02-17T09:00:00Z",
        "duration": "15 mins",
        "participants": ["naveen@neuralnotes.ai", "bob@company.com"],
        "status": "completed",
        "tags": ["engineering", "standup"],
        "summary": "Team unblocked on auth module. Redis integration in progress. Tests passing.",
        "action_items": [
            {"task": "Finish Redis integration", "assignee": "Bob", "due": "2026-02-19"},
        ],
        "sentiment": "neutral",
    },
    {
        "id": "mtg_003",
        "title": "Client Demo Prep",
        "date": "2026-02-16T14:00:00Z",
        "duration": "30 mins",
        "participants": ["naveen@neuralnotes.ai", "carol@company.com"],
        "status": "completed",
        "tags": ["demo", "client", "sales"],
        "summary": "Demo script finalized. Slides reviewed. Live recording feature will be highlighted.",
        "action_items": [
            {"task": "Polish demo slides", "assignee": "Carol", "due": "2026-02-18"},
            {"task": "Test live recording on client machine", "assignee": "Naveen", "due": "2026-02-18"},
        ],
        "sentiment": "positive",
    },
]


@app.get("/v1/meetings", tags=["Meetings"])
def mock_list_meetings():
    return {
        "status": "success",
        "total": len(MOCK_MEETINGS),
        "meetings": MOCK_MEETINGS,
        "note": "🟡 Mock data — Firebase not connected yet",
    }


@app.get("/v1/meetings/{meeting_id}", tags=["Meetings"])
def mock_get_meeting(meeting_id: str):
    meeting = next((m for m in MOCK_MEETINGS if m["id"] == meeting_id), None)
    if not meeting:
        return {"error": "Meeting not found", "id": meeting_id}
    return {"status": "success", "meeting": meeting}


@app.post("/v1/meetings/upload", tags=["Meetings"])
def mock_upload_meeting():
    return {
        "status": "success",
        "message": "✅ Mock upload received (Whisper not connected yet)",
        "meeting_id": "mtg_mock_999",
        "estimated_processing_seconds": 120,
        "pipeline_stages": [
            "audio_processing  → 🟡 pending",
            "transcription     → 🟡 pending",
            "diarization       → 🟡 pending",
            "ai_analysis       → 🟡 pending",
            "embedding         → 🟡 pending",
        ]
    }


@app.post("/v1/meetings/{meeting_id}/query", tags=["Meetings"])
def mock_query_meeting(meeting_id: str):
    return {
        "status": "success",
        "answer": "✅ Mock answer — The team decided to push the product launch to Q4 due to resource constraints.",
        "sources": [
            {
                "speaker": "Naveen",
                "text": "I think we should move the launch to Q4 to give us more runway.",
                "timestamp": 342.5,
            }
        ],
        "note": "🟡 Mock response — RAG pipeline not connected yet",
    }


# ── Mock Stats Endpoint ──────────────────────────────────────
@app.get("/v1/stats", tags=["Dashboard"])
def mock_stats():
    return {
        "total_meetings": 3,
        "total_hours_recorded": 1.5,
        "total_action_items": 5,
        "completed_action_items": 2,
        "most_discussed_topics": ["planning", "engineering", "demo"],
        "avg_meeting_duration_mins": 30,
        "note": "🟡 Mock data — Firebase not connected yet",
    }