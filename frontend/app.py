# ============================================================
#  NeuralNotes — Streamlit Frontend
#  Run: streamlit run frontend/app.py
# ============================================================

import streamlit as st
import requests
from datetime import datetime

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="NeuralNotes",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; color: #fff; }

    .nn-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .nn-header h1 { color: white; font-size: 2.5rem; margin: 0; }
    .nn-header p  { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin: 0.5rem 0 0 0; }

    .metric-card {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #667eea; }
    .metric-label { font-size: 0.85rem; color: #888; margin-top: 0.3rem; }

    .meeting-card {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-left: 4px solid #667eea;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .meeting-title { font-size: 1.1rem; font-weight: bold; color: #fff; }
    .meeting-meta  { font-size: 0.82rem; color: #888; margin-top: 0.3rem; }

    .tag {
        display: inline-block;
        background: #2d3250;
        color: #667eea;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 2px;
    }

    .utterance-row {
        background: #1a1d2e;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin: 0.4rem 0;
        border-left: 3px solid #667eea;
    }
    .utterance-time  { color: #667eea; font-size: 0.78rem; font-weight: bold; }
    .utterance-speaker { color: #a78bfa; font-size: 0.82rem; font-weight: bold; }
    .utterance-text  { color: #ddd; font-size: 0.92rem; margin-top: 0.2rem; }

    .success-banner {
        background: linear-gradient(135deg, #1a472a, #2d6a4f);
        border: 1px solid #40916c;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .stat-pill {
        display: inline-block;
        background: #2d3250;
        color: #a78bfa;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────
def format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format for display."""
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def call_api(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=3)
        return r.json()
    except Exception:
        return None


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 NeuralNotes")
    st.markdown("*AI Meeting Intelligence*")
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🎙️ Upload Meeting", "🔍 Ask NeuralNotes", "⚙️ System Status"],
        label_visibility="collapsed",
    )

    st.divider()

    health = call_api("/health")
    if health:
        st.markdown("**API Status**")
        st.markdown("🟢 Backend Online")
        st.markdown(f"**Whisper:** {health['services']['whisper']}")
    else:
        st.error("🔴 Backend Offline\n\nRun:\n`uvicorn backend.main:app --reload`")

    st.divider()
    st.caption("Phase 1 — Transcription ✅\nPhase 2 — AI Analysis 🔜\nPhase 3 — Dashboard 🔜\nPhase 4 — Q&A RAG 🔜\nPhase 5 — Integrations 🔜")


# ════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":

    st.markdown("""
    <div class="nn-header">
        <h1>🧠 NeuralNotes</h1>
        <p>Turn every conversation into intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # Show last transcription result if stored in session
    if "last_transcript" in st.session_state:
        t = st.session_state["last_transcript"]
        st.markdown("### 📋 Last Processed Meeting")
        st.markdown(f"""
        <div class="meeting-card">
            <div class="meeting-title">📅 {t['title']}</div>
            <div class="meeting-meta">
                🎵 {t['filename']} &nbsp;|&nbsp;
                ⏱️ {format_time(t['transcript']['duration_seconds'])} &nbsp;|&nbsp;
                📝 {t['transcript']['word_count']} words &nbsp;|&nbsp;
                🌐 {t['transcript']['language'].upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 View Full Transcript"):
            st.session_state["view_transcript"] = True
            st.session_state["page_override"] = "upload"
            st.rerun()
    else:
        st.info("👆 No meetings yet! Go to **🎙️ Upload Meeting** to transcribe your first meeting.")

    st.markdown("### 🚀 What NeuralNotes Does")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">🎙️</div>
            <div class="metric-label">Transcribes audio with 95%+ accuracy</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">🧠</div>
            <div class="metric-label">Summarizes with Claude AI (Phase 2)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">✅</div>
            <div class="metric-label">Extracts action items (Phase 2)</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-card">
            <div class="metric-value">🔍</div>
            <div class="metric-label">Q&A on meetings (Phase 4)</div>
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE: UPLOAD MEETING
# ════════════════════════════════════════════════════════════
elif page == "🎙️ Upload Meeting":

    # If viewing a transcript result
    if st.session_state.get("view_transcript") and "last_transcript" in st.session_state:
        data = st.session_state["last_transcript"]
        transcript = data["transcript"]

        # Success banner
        st.markdown(f"""
        <div class="success-banner">
            <h3 style="color:#4caf50; margin:0">✅ Transcription Complete!</h3>
            <p style="color:#ccc; margin:0.4rem 0 0 0">{data['title']} — {data['filename']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{format_time(transcript['duration_seconds'])}</div>
                <div class="metric-label">Duration</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{transcript['word_count']}</div>
                <div class="metric-label">Words</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{len(transcript['utterances'])}</div>
                <div class="metric-label">Segments</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{data['processing']['processing_time_s']}s</div>
                <div class="metric-label">Processing Time</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs for different views
        tab1, tab2 = st.tabs(["📝 Full Transcript", "🕐 Timestamped Segments"])

        with tab1:
            st.markdown("### Full Transcript")
            st.markdown(f"""
            <div style="background:#1e2130; border-radius:10px; padding:1.5rem;
                        line-height:1.8; color:#ddd; font-size:0.95rem;">
                {transcript['full_text']}
            </div>
            """, unsafe_allow_html=True)

            # Copy button workaround
            st.text_area("Copy transcript text:", transcript['full_text'], height=200)

        with tab2:
            st.markdown("### Timestamped Segments")
            st.caption("Each segment shows exactly when it was spoken")
            for utt in transcript['utterances']:
                st.markdown(f"""
                <div class="utterance-row">
                    <span class="utterance-time">⏱ {format_time(utt['start_time'])} → {format_time(utt['end_time'])}</span>
                    &nbsp;&nbsp;
                    <span class="utterance-speaker">🎙 {utt['speaker']}</span>
                    <div class="utterance-text">{utt['text']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Upload Another Meeting", use_container_width=True):
                st.session_state.pop("view_transcript", None)
                st.rerun()
        with col2:
            st.info("🔜 Phase 2: Claude will auto-generate summary & action items from this transcript!")

    # Upload form
    else:
        st.markdown("## 🎙️ Upload a Meeting")
        st.caption("Upload any audio or video file — NeuralNotes will transcribe it instantly")

        with st.form("upload_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input(
                    "Meeting Title",
                    placeholder="e.g. Q3 Planning Session"
                )
            with col2:
                participants = st.text_input(
                    "Participants (comma separated)",
                    placeholder="alice@co.com, bob@co.com"
                )

            language = st.selectbox(
                "Language",
                ["auto", "en", "hi", "es", "fr", "de", "ja", "zh"],
                format_func=lambda x: {
                    "auto": "🌐 Auto Detect",
                    "en": "🇺🇸 English",
                    "hi": "🇮🇳 Hindi",
                    "es": "🇪🇸 Spanish",
                    "fr": "🇫🇷 French",
                    "de": "🇩🇪 German",
                    "ja": "🇯🇵 Japanese",
                    "zh": "🇨🇳 Chinese",
                }[x]
            )

            uploaded_file = st.file_uploader(
                "Upload Audio / Video File",
                type=["mp3", "mp4", "wav", "m4a", "ogg", "webm", "flac"],
                help="Supported formats: MP3, MP4, WAV, M4A, OGG, WEBM, FLAC — Max 500MB"
            )

            submit = st.form_submit_button(
                "🚀 Transcribe Meeting",
                use_container_width=True
            )

            if submit:
                if not uploaded_file:
                    st.error("⚠️ Please upload an audio file first!")
                elif not title.strip():
                    st.error("⚠️ Please enter a meeting title!")
                else:
                    with st.spinner(f"🎙️ Transcribing '{title}'... this may take a moment"):
                        try:
                            response = requests.post(
                                f"{API_URL}/v1/meetings/upload",
                                files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                                data={
                                    "title": title,
                                    "participants": participants,
                                    "language": language,
                                },
                                timeout=300,  # 5 min timeout for long audio
                            )

                            if response.status_code == 200:
                                result = response.json()
                                # Store result in session state
                                st.session_state["last_transcript"] = result
                                st.session_state["view_transcript"] = True
                                st.rerun()
                            else:
                                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot reach backend. Make sure it's running:\n`uvicorn backend.main:app --reload`")
                        except Exception as e:
                            st.error(f"❌ Something went wrong: {str(e)}")


# ════════════════════════════════════════════════════════════
# PAGE: ASK NEURALNOTES
# ════════════════════════════════════════════════════════════
elif page == "🔍 Ask NeuralNotes":
    st.markdown("## 🔍 Ask NeuralNotes")

    st.info("🔜 Coming in **Phase 4** — RAG-powered Q&A. You'll be able to ask anything about any meeting and get instant answers with timestamps.")

    st.markdown("### Preview of what's coming:")
    st.markdown("""
    ```
    You:          "What did we decide about John Smith?"
    NeuralNotes:  "The team decided to connect John with the guidance
                   counselor and find childcare resources for his family."
                   📍 Source: 01:09 — 01:31
    ```
    """)


# ════════════════════════════════════════════════════════════
# PAGE: SYSTEM STATUS
# ════════════════════════════════════════════════════════════
elif page == "⚙️ System Status":
    st.markdown("## ⚙️ System Status")

    health = call_api("/health")
    if health:
        st.success("✅ Backend API is online!")
        st.markdown("### Services")
        for service, status in health["services"].items():
            st.markdown(f"**{service.capitalize()}:** {status}")
    else:
        st.error("❌ Backend API is not reachable.\n\nRun: `uvicorn backend.main:app --reload --port 8000`")

    st.divider()
    st.markdown("### 📦 Build Info")
    st.markdown(f"- **App:** NeuralNotes v1.0.0")
    st.markdown(f"- **Phase:** 1 — Transcription ✅")
    st.markdown(f"- **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.markdown(f"- **Next:** Phase 2 — Claude AI Analysis")