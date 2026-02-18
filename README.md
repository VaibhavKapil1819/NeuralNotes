# 🧠 NeuralNotes
### *Turn every conversation into intelligence*

> An enterprise-grade AI Meeting Intelligence Platform that automatically records, transcribes, summarizes, and extracts actionable insights from meetings.

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red?logo=streamlit)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)
![Claude](https://img.shields.io/badge/AI-Claude%203.5-purple)
![Whisper](https://img.shields.io/badge/ASR-Whisper-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📋 Table of Contents

- [What is NeuralNotes?](#-what-is-neuralnotes)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [Firebase Setup](#-firebase-setup)
- [Running the App](#-running-the-app)
- [API Documentation](#-api-documentation)
- [Development Guide](#-development-guide)
- [Roadmap](#-roadmap)

---

## 🤔 What is NeuralNotes?

NeuralNotes is an AI-powered meeting intelligence platform that eliminates manual note-taking forever. Upload any meeting recording or record live — NeuralNotes handles the rest:

- 🎙️ **Transcribes** audio with speaker labels using OpenAI Whisper
- 🧠 **Summarizes** meetings and extracts action items using Claude AI
- 🔍 **Answers questions** about any meeting using RAG (e.g. *"What did we decide about the budget?"*)
- 📧 **Emails** formatted summaries to all participants automatically
- 📊 **Tracks** all your meetings in a beautiful searchable dashboard

---

## ✨ Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| Audio Upload | MP3, MP4, WAV, M4A support up to 500MB | ✅ Phase 1 |
| Transcription | Whisper-powered with 95%+ accuracy | ✅ Phase 1 |
| Smart Summary | AI-generated structured meeting summary | ✅ Phase 2 |
| Action Items | Auto-extracted tasks with assignees & deadlines | ✅ Phase 2 |
| Speaker Labels | Identify who said what (diarization) | ✅ Phase 2 |
| Meeting Dashboard | Searchable history of all meetings | ✅ Phase 3 |
| Q&A on Meetings | Ask anything, get answers with timestamps | ✅ Phase 4 |
| Email Summaries | Auto-send to participants via SendGrid | ✅ Phase 5 |
| Slack Integration | Post summaries to channels | 🔄 Phase 5 |
| Multi-language | Support for 10+ languages | 🔄 Phase 5 |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                           │
│              Streamlit Web UI  (port 8501)                  │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
┌───────────────────────────▼─────────────────────────────────┐
│                     API GATEWAY                             │
│              FastAPI Backend  (port 8000)                   │
│         Auth │ Rate Limiting │ CORS │ Routing               │
└──────┬──────────────┬───────────────────┬───────────────────┘
       │              │                   │
┌──────▼──────┐ ┌─────▼──────┐ ┌─────────▼──────┐
│   Audio     │ │    AI      │ │  Integration   │
│  Service    │ │  Service   │ │   Service      │
│             │ │            │ │                │
│ ffmpeg      │ │ Whisper    │ │ SendGrid       │
│ pydub       │ │ Claude API │ │ Slack          │
│ pyannote    │ │ ChromaDB   │ │ Google Cal     │
└──────┬──────┘ └─────┬──────┘ └────────────────┘
       │              │
┌──────▼──────────────▼───────────────────────────────────────┐
│                      DATA LAYER                             │
│  Firebase Firestore   │   ChromaDB        │  Firebase       │
│  (meetings, users)    │   (embeddings)    │  Storage        │
│                       │   (RAG Q&A)       │  (audio files)  │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow (Meeting Upload)

```
User uploads audio
      ↓
FastAPI receives file → validates size & format
      ↓
Audio Service → ffmpeg converts to 16kHz WAV
      ↓
Whisper Engine → transcribes audio to text
      ↓
Speaker Engine → diarization (who said what)
      ↓
Claude Engine → summary + action items + decisions
      ↓
Vector Store → chunk & embed transcript for Q&A
      ↓
Firebase Firestore → save all results
      ↓
SendGrid → email summary to participants
      ↓
Streamlit UI → display results to user
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.13+ | Core language |
| Web Framework | FastAPI | REST API backend |
| Frontend | Streamlit | Web dashboard UI |
| Transcription | OpenAI Whisper | Speech to text |
| LLM | Anthropic Claude 3.5 | Summarization & Q&A |
| Diarization | pyannote.audio | Speaker identification |
| Vector DB | ChromaDB | RAG-based Q&A |
| Database | Firebase Firestore | Cloud NoSQL database |
| Storage | Firebase Storage | Audio file storage |
| Auth | Firebase Auth | User authentication |
| Email | SendGrid | Meeting summary emails |
| Notifications | Slack SDK | Slack integration |
| Audio | ffmpeg + pydub | Audio processing |
| Task Queue | Celery + Redis | Async job processing |
| Monitoring | Loguru + Sentry | Logging & error tracking |

---

## 📁 Project Structure

```
neuralnotes/
│
├── backend/                        # FastAPI backend
│   ├── main.py                     # App entry point, routes registration
│   ├── config/
│   │   ├── settings.py             # All env variables loaded here
│   │   └── firebase.py             # Firebase initialization
│   ├── routes/
│   │   ├── auth.py                 # /auth/* endpoints
│   │   ├── meetings.py             # /meetings/* endpoints
│   │   └── query.py                # /query/* endpoints (RAG)
│   ├── services/
│   │   ├── audio_service.py        # Audio processing logic
│   │   ├── ai_service.py           # Claude API calls
│   │   ├── email_service.py        # SendGrid email sending
│   │   └── firebase_service.py     # Firestore CRUD operations
│   ├── models/
│   │   ├── meeting.py              # Meeting Pydantic models
│   │   ├── user.py                 # User Pydantic models
│   │   └── analysis.py             # Analysis Pydantic models
│   ├── middleware/
│   │   └── auth_middleware.py      # JWT validation middleware
│   └── utils/
│       └── helpers.py              # Shared utility functions
│
├── ai_pipeline/                    # AI/ML pipeline
│   ├── transcription/
│   │   └── whisper_engine.py       # Whisper transcription
│   ├── diarization/
│   │   └── speaker_engine.py       # Speaker diarization
│   ├── analysis/
│   │   └── claude_engine.py        # Claude summarization
│   └── rag/
│       ├── vector_store.py         # ChromaDB operations
│       └── query_engine.py         # RAG Q&A engine
│
├── frontend/                       # Streamlit UI
│   ├── app.py                      # Main Streamlit entry point
│   ├── pages/
│   │   ├── login.py                # Login / Register page
│   │   ├── dashboard.py            # Meeting history dashboard
│   │   └── meeting_detail.py       # Individual meeting view
│   └── components/
│       └── meeting_card.py         # Reusable meeting card component
│
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
│
├── docs/                           # Additional documentation
├── temp/                           # Temporary audio files (gitignored)
├── chroma_db/                      # ChromaDB local storage (gitignored)
│
├── .env                            # Your secrets (never commit this!)
├── .env.example                    # Template — safe to commit
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
├── setup.sh                        # One-command setup script
├── Dockerfile                      # Docker container config
├── docker-compose.yml              # Multi-service Docker setup
└── README.md                       # You are here!
```

---

## ⚡ Quick Start

### Prerequisites

Make sure you have these installed on your machine:

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.13+ | [python.org](https://python.org) |
| Git | Latest | [git-scm.com](https://git-scm.com) |
| ffmpeg | Latest | `brew install ffmpeg` |
| Redis | Latest | `brew install redis` |

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/neuralnotes.git
cd neuralnotes
```

### 2. Run the setup script (does everything automatically)

```bash
chmod +x setup.sh
./setup.sh
```

**OR set up manually:**

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys (see [Environment Variables](#-environment-variables) section).

### 4. Set up Firebase

See the [Firebase Setup](#-firebase-setup) section below.

### 5. Start the application

```bash
# Terminal 1 — Start backend
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Start frontend
streamlit run frontend/app.py
```

Open your browser:
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and fill in these values:

```bash
cp .env.example .env
```

| Variable | Required | Where to get it |
|----------|----------|----------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | [console.anthropic.com](https://console.anthropic.com) |
| `OPENAI_API_KEY` | ✅ Yes | [platform.openai.com](https://platform.openai.com) |
| `FIREBASE_CREDENTIALS_PATH` | ✅ Yes | Firebase Console → Service Account |
| `FIREBASE_PROJECT_ID` | ✅ Yes | Firebase Console → Project Settings |
| `SENDGRID_API_KEY` | ⚠️ Optional | [sendgrid.com](https://sendgrid.com) |
| `SLACK_WEBHOOK_URL` | ⚠️ Optional | Slack App settings |
| `SECRET_KEY` | ✅ Yes | Run: `openssl rand -hex 32` |
| `REDIS_URL` | ✅ Yes | `redis://localhost:6379` (default) |

---

## 🔥 Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click **"Add Project"** → name it `neuralnotes-app`
3. **Enable Firestore:**
   - Go to Firestore Database → Create Database → Start in test mode
4. **Enable Authentication:**
   - Go to Authentication → Sign-in method → Enable Email/Password and Google
5. **Enable Storage:**
   - Go to Storage → Get Started
6. **Get Service Account Key:**
   - Project Settings → Service Accounts → Generate New Private Key
   - Save the downloaded JSON as `firebase_credentials.json` in the project root
7. Update your `.env`:
   ```
   FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
   FIREBASE_PROJECT_ID=neuralnotes-app
   ```

---

## 🚀 Running the App

### Development Mode

```bash
# Activate virtual environment first!
source venv/bin/activate

# Start Redis (required for task queue)
brew services start redis

# Terminal 1 — Backend API
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend UI
streamlit run frontend/app.py

# Terminal 3 — Celery worker (for async audio processing)
celery -A backend.celery_app worker --loglevel=info
```

### Verify everything is running

```
✅ Backend API:     http://localhost:8000
✅ API Docs:        http://localhost:8000/docs
✅ Frontend UI:     http://localhost:8501
✅ Redis:           redis://localhost:6379
```

---

## 📖 API Documentation

FastAPI auto-generates interactive API docs. Once the backend is running visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

```
POST   /v1/auth/register          Register new user
POST   /v1/auth/login             Login
GET    /v1/auth/me                Get current user

POST   /v1/meetings/upload        Upload & process meeting audio
GET    /v1/meetings               List all meetings
GET    /v1/meetings/{id}          Get meeting details
GET    /v1/meetings/{id}/status   Check processing status
POST   /v1/meetings/{id}/query    Ask a question about a meeting
POST   /v1/meetings/{id}/email    Send summary email
```

---

## 👨‍💻 Development Guide

### Code Style

We use Black for formatting and Ruff for linting:

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy backend/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/unit/test_audio_service.py
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, then commit
git add .
git commit -m "feat: add whisper transcription engine"

# Push and create PR
git push origin feature/your-feature-name
```

### Commit Message Format

```
feat:     New feature
fix:      Bug fix
docs:     Documentation change
refactor: Code refactor
test:     Adding tests
chore:    Build/config changes
```

---

## 🗺️ Roadmap

- [x] Project setup & configuration
- [ ] **Phase 1** — Audio upload + Whisper transcription
- [ ] **Phase 2** — Claude summarization + action items + speaker diarization
- [ ] **Phase 3** — Streamlit dashboard + Firebase auth
- [ ] **Phase 4** — RAG Q&A system with ChromaDB
- [ ] **Phase 5** — Email, Slack, multi-language, Docker deployment

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">Built with ❤️ by Naveen | NeuralNotes — Where meetings become knowledge</p>
