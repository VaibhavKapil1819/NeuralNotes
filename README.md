# 🧠 NeuralNotes
### *Turn every conversation into intelligence*

> An enterprise-grade AI Meeting Intelligence Platform that automatically records, transcribes, summarizes, and extracts actionable insights from meetings.
![TypeScript](https://img.shields.io/badge/TypeScript-Auto-blue?logo=typescript)
![Next.js](https://img.shields.io/badge/Next.js-15+-black?logo=nextdotjs)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Optional-38B2AC?logo=tailwindcss)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Firebase](https://img.shields.io/badge/Firebase-Auth%20%7C%20Firestore-orange?logo=firebase)
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

---

## 🤔 What is NeuralNotes?

NeuralNotes is an enterprise-grade AI meeting intelligence platform that eliminates manual note-taking. Built with a modern **Next.js 15** frontend and a high-performance **FastAPI** backend, it handles the end-to-end meeting lifecycle:

- 🎙️ **Transcribes** audio with 95%+ accuracy using OpenAI Whisper.
- 🧠 **Summarizes** meetings and extracts action items using Claude 3.5 Sonnet.
- 🔍 **Intelligent Q&A** ask anything about your meeting history via RAG.
- 🛡️ **Secure** production-ready authentication via Firebase Auth (Google & Email).

---

## ✨ Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| Audio Upload | Drag-and-drop support for MP3, WAV, M4A | ✅ Phase 1 |
| Transcription | Whisper-powered with speaker identification | ✅ Phase 1 |
| Premium UI | Dark mode, glassmorphism, responsive Next.js app | ✅ Phase 1 |
| Full Auth | Secure login/register with Google & Email | ✅ Phase 1 |
| Smart Summary | AI-generated structured analysis | ✅ Phase 2 |
| Action Items | Auto-extracted tasks and decisions | ✅ Phase 2 |
| Dashboard | Searchable meeting library | 🔄 Phase 3 |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                         │
│              Next.js 15 App (port 3000)                     │
│         Firebase Client SDK │ AuthContext │ React           │
└───────────────────────────┬─────────────────────────────────┘
                            │ Secure REST API (JWT)
┌───────────────────────────▼─────────────────────────────────┐
│                     BACKEND SERVICE                         │
│              FastAPI Backend (port 8000)                    │
│         Firebase Admin SDK │ Auth Middleware │ Pydantic     │
└──────┬──────────────┬───────────────────┬───────────────────┘
       │              │                   │
┌──────▼──────┐ ┌─────▼──────┐ ┌─────────▼──────┐
│   Audio     │ │    AI      │ │  Persistence   │
│  Service    │ │  Service   │ │    Layer       │
│             │ │            │ │                │
│ Whisper     │ │ Claude 3.5 │ │ Firestore      │
│ ffmpeg      │ │ ChromaDB   │ │ Firebase Store │
└──────┴──────┘ └─────┬──────┘ └────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 15 (App Router) | Modern, fast web UI |
| Styling | Vanilla CSS / CSS Modules | Premium, custom design |
| Auth | Firebase Auth | Secure multi-provider login |
| Backend | FastAPI | High-performance Python API |
| Transcription | OpenAI Whisper | Local/Cloud speech-to-text |
| LLM | Anthropic Claude 3.5 | Summarization & Insights |
| Database | Firebase Firestore | NoSQL Real-time database |
| Storage | Firebase Storage | Meeting audio persistence |
| Vector DB | ChromaDB | RAG-based search & Q&A |

---

## 📁 Project Structure

```
neuralnotes/
├── frontend/                # Next.js 15 Application
│   ├── src/app/             # Pages & Layouts
│   ├── src/context/         # AuthContext state
│   ├── src/lib/             # Firebase SDK init
│   └── src/components/      # UI components
├── backend/                 # FastAPI API
│   ├── config/              # firebase_admin & settings
│   ├── middleware/          # JWT validation logic
│   └── routes/              # Meeting & Auth endpoints
├── ai_pipeline/             # ML core
│   ├── transcription/       # Whisper engine
│   └── analysis/            # Claude integration
└── requirements.txt         # Backend dependencies
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

or 
python -m streamlit run frontend/app.py

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

<p align="center">Built with ❤️ by Vaibhav | NeuralNotes — Where meetings become knowledge</p>
