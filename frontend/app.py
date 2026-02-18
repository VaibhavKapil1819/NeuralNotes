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

# ── Constants ────────────────────────────────────────────────
API_URL = "http://localhost:8000"

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Header */
    .nn-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .nn-header h1 { color: white; font-size: 2.5rem; margin: 0; }
    .nn-header p  { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin: 0.5rem 0 0 0; }

    /* Metric cards */
    .metric-card {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #667eea; }
    .metric-label { font-size: 0.85rem; color: #888; margin-top: 0.3rem; }

    /* Meeting card */
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
    .badge-positive { color: #4caf50; font-weight: bold; }
    .badge-neutral  { color: #ffc107; font-weight: bold; }
    .badge-negative { color: #f44336; font-weight: bold; }

    /* Status pill */
    .status-online  { color: #4caf50; font-weight: bold; }
    .status-mock    { color: #ffc107; font-weight: bold; }

    /* Action item */
    .action-item {
        background: #16213e;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ─────────────────────────────────────────
def call_api(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=3)
        return r.json()
    except Exception:
        return None


def sentiment_badge(sentiment):
    if sentiment == "positive":
        return '<span class="badge-positive">😊 Positive</span>'
    elif sentiment == "negative":
        return '<span class="badge-negative">😟 Negative</span>'
    else:
        return '<span class="badge-neutral">😐 Neutral</span>'


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 NeuralNotes")
    st.markdown("*AI Meeting Intelligence*")
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🎙️ New Meeting", "🔍 Ask NeuralNotes", "⚙️ System Status"],
        label_visibility="collapsed",
    )

    st.divider()

    # API Health
    health = call_api("/health")
    if health:
        st.markdown("**API Status**")
        st.markdown('<span class="status-online">🟢 Backend Online</span>', unsafe_allow_html=True)
    else:
        st.markdown("**API Status**")
        st.error("🔴 Backend Offline\nRun: `uvicorn backend.main:app --reload`")

    st.divider()
    st.markdown("**Mock Mode** 🟡")
    st.caption("Firebase & AI not connected yet.\nAll data is mock for now.")


# ── Pages ─────────────────────────────────────────────────────

# ── Dashboard ───────────────────────────────────────────────
if page == "🏠 Dashboard":

    # Header
    st.markdown("""
    <div class="nn-header">
        <h1>🧠 NeuralNotes</h1>
        <p>Turn every conversation into intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    stats = call_api("/v1/stats")
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_meetings']}</div>
                <div class="metric-label">Total Meetings</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_hours_recorded']}h</div>
                <div class="metric-label">Hours Recorded</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['total_action_items']}</div>
                <div class="metric-label">Action Items</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats['avg_meeting_duration_mins']}m</div>
                <div class="metric-label">Avg Duration</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Search
    search = st.text_input("🔍 Search meetings...", placeholder="Type to search by title or topic")

    # Meeting list
    st.markdown("### 📋 Recent Meetings")

    data = call_api("/v1/meetings")
    if data and "meetings" in data:
        meetings = data["meetings"]
        if search:
            meetings = [m for m in meetings if search.lower() in m["title"].lower()
                        or any(search.lower() in t for t in m["tags"])]

        if not meetings:
            st.info("No meetings found matching your search.")
        else:
            for m in meetings:
                tags_html = "".join([f'<span class="tag">#{t}</span>' for t in m["tags"]])
                with st.container():
                    st.markdown(f"""
                    <div class="meeting-card">
                        <div class="meeting-title">📅 {m['title']}</div>
                        <div class="meeting-meta">
                            🕐 {m['date'][:10]}  &nbsp;|&nbsp;
                            ⏱️ {m['duration']}  &nbsp;|&nbsp;
                            👥 {len(m['participants'])} participants &nbsp;|&nbsp;
                            {sentiment_badge(m['sentiment'])}
                        </div>
                        <div style="margin-top: 0.6rem; color: #ccc; font-size: 0.9rem;">
                            {m['summary']}
                        </div>
                        <div style="margin-top: 0.6rem;">{tags_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander(f"📋 Action Items ({len(m['action_items'])})"):
                        for item in m["action_items"]:
                            st.markdown(f"""
                            <div class="action-item">
                                ☐ &nbsp;<b>{item['task']}</b><br>
                                <span style="color:#888; font-size:0.8rem;">
                                    👤 {item['assignee']} &nbsp;|&nbsp; 📅 Due: {item['due']}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.warning("Could not reach the backend API. Make sure it's running!")


# ── New Meeting ──────────────────────────────────────────────
elif page == "🎙️ New Meeting":
    st.markdown("## 🎙️ Upload a Meeting")
    st.caption("Upload an audio/video file to transcribe and analyze")

    with st.form("upload_form"):
        title = st.text_input("Meeting Title", placeholder="e.g. Q3 Planning Session")
        participants = st.text_input("Participants (comma separated)", placeholder="alice@co.com, bob@co.com")
        language = st.selectbox("Language", ["Auto Detect", "English", "Hindi", "Spanish", "French", "German"])
        uploaded_file = st.file_uploader(
            "Upload Audio/Video",
            type=["mp3", "mp4", "wav", "m4a", "ogg", "webm"],
            help="Max 500MB"
        )
        submit = st.form_submit_button("🚀 Process Meeting", use_container_width=True)

        if submit:
            if not uploaded_file:
                st.error("Please upload an audio file first!")
            else:
                with st.spinner("Processing your meeting... (mock mode)"):
                    import time
                    time.sleep(2)
                    result = requests.post(f"{API_URL}/v1/meetings/upload").json()

                st.success("✅ Meeting received!")
                st.json(result)
                st.info("🟡 Mock mode: Real transcription will happen once Whisper is connected in Phase 1.")


# ── Ask NeuralNotes ──────────────────────────────────────────
elif page == "🔍 Ask NeuralNotes":
    st.markdown("## 🔍 Ask NeuralNotes")
    st.caption("Ask anything about your meetings in natural language")

    data = call_api("/v1/meetings")
    meetings = data["meetings"] if data else []
    meeting_options = {m["title"]: m["id"] for m in meetings}

    selected = st.selectbox("Select a meeting", list(meeting_options.keys()))
    question = st.text_input("Your question", placeholder="What did we decide about the budget?")

    if st.button("🧠 Ask", use_container_width=True):
        if not question:
            st.warning("Please type a question first!")
        else:
            with st.spinner("Searching through meeting knowledge..."):
                import time
                time.sleep(1)
                result = requests.post(
                    f"{API_URL}/v1/meetings/{meeting_options[selected]}/query"
                ).json()

            st.markdown("### 💡 Answer")
            st.success(result["answer"])

            st.markdown("### 📌 Source")
            for src in result["sources"]:
                st.markdown(f"""
                <div class="action-item">
                    🗣️ <b>{src['speaker']}</b> at <b>{src['timestamp']}s</b><br>
                    <i>"{src['text']}"</i>
                </div>
                """, unsafe_allow_html=True)

            st.info("🟡 Mock mode: Real RAG-powered answers will work once Phase 4 is complete.")


# ── System Status ────────────────────────────────────────────
elif page == "⚙️ System Status":
    st.markdown("## ⚙️ System Status")

    health = call_api("/health")
    if health:
        st.success("Backend API is reachable!")
        st.markdown("### Service Health")
        for service, status in health["services"].items():
            st.markdown(f"**{service.capitalize()}:** {status}")
    else:
        st.error("Backend API is not reachable. Run: `uvicorn backend.main:app --reload`")

    st.divider()
    st.markdown("### 📦 Build Info")
    st.markdown(f"- **App Version:** 1.0.0")
    st.markdown(f"- **Mode:** 🟡 Mock (Phase 0)")
    st.markdown(f"- **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    st.markdown(f"- **Next Step:** Phase 1 — Wire up Whisper transcription")