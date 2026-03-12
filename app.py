"""
PakJurist - Pakistan Legal Awareness System
Production-grade Streamlit chatbot with working TTS speak/pause/stop controls
"""

import streamlit as st
import uuid
import json
import re
import base64
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
import streamlit.components.v1 as components

from agent import LegalAgent, ProcessedDocument
from database import Database

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PakJurist — Pakistan Legal Awareness",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    font-family: 'Sora', sans-serif;
    color: #dde3f0;
}

/* Emoji font — renders correctly on all Windows browsers */
* {
    font-family: 'Sora', "Segoe UI Emoji", "Apple Color Emoji",
                 "Noto Color Emoji", sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── SIDEBAR — Force visible and styled ── */
[data-testid="stSidebar"] {
    background: #0c1220 !important;
    border-right: 1px solid #1a2540 !important;
    min-width: 260px !important;
    max-width: 300px !important;
    display: block !important;
    visibility: visible !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: #0c1220 !important;
    padding: 0 !important;
}
/* Force sidebar open on all screen sizes */
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"][aria-expanded="false"] {
    margin-left: 0 !important;
    transform: none !important;
}

/* Brand */
.sidebar-brand {
    background: linear-gradient(135deg, #0f2027 0%, #1a3a5c 100%);
    padding: 1.4rem 1.2rem 1.1rem;
    border-bottom: 1px solid #1e3356;
}
.sidebar-brand-icon {
    font-size: 2.2rem;
    line-height: 1;
    display: block;
    margin-bottom: 0.5rem;
}
.sidebar-brand h1 {
    font-size: 1.0rem !important;
    font-weight: 700;
    color: #e8f0fe !important;
    line-height: 1.35;
    margin: 0 0 0.2rem !important;
}
.sidebar-brand p {
    font-size: 0.71rem;
    color: #5a7fa8;
    margin: 0 !important;
    font-family: 'JetBrains Mono', monospace;
}

/* Section label rows */
.section-label-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.8rem 1rem 0.35rem;
    border-top: 1px solid #111d30;
    margin-top: 0.1rem;
}
.section-label-icon { font-size: 0.9rem; flex-shrink: 0; }
.section-label-text {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    color: #3b5a7a;
    font-family: 'JetBrains Mono', monospace;
}
.section-pad { padding: 0 0 0.5rem; }

/* Radio */
[data-testid="stSidebar"] .stRadio label {
    color: #8ba8c8 !important;
    font-size: 0.86rem !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: #0a1525 !important;
    border: 1.5px dashed #1e3a5f !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploadDropzone"] > div { color: #5a7fa8 !important; font-size: 0.8rem !important; }

.file-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #0f2040;
    border: 1px solid #1e4080;
    color: #7ab3e0;
    padding: 0.22rem 0.6rem;
    border-radius: 20px;
    font-size: 0.76rem;
    margin: 0.2rem 0.15rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: #0f1e35 !important;
    color: #7ab3e0 !important;
    border: 1px solid #1a3356 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    font-family: 'Sora', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #142844 !important;
    border-color: #2a5080 !important;
    color: #a8d4f5 !important;
}

/* Stats */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.32rem 1rem;
    font-size: 0.82rem;
    color: #5a7fa8;
    border-bottom: 1px solid #0f1e35;
}
.stat-row:last-child { border-bottom: none; }
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.86rem;
    color: #7ab3e0;
    font-weight: 600;
}

/* Disclaimer */
.disclaimer {
    background: #0a0f1a;
    border-left: 3px solid #c0392b;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 0.74rem;
    color: #5a6a80;
    line-height: 1.6;
    margin: 0.6rem 0.8rem 1rem;
}
.disclaimer strong { color: #e74c3c; }

/* ── Main area ── */
.main .block-container {
    padding: 1.5rem 2.2rem 5rem !important;
    max-width: 1060px !important;
}

/* Top banner */
.top-banner {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: linear-gradient(110deg, #0d1b2e 0%, #091526 60%, #07101f 100%);
    border: 1px solid #1a2e4a;
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.6rem;
    overflow: hidden;
    position: relative;
}
.top-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(30,80,160,0.14) 0%, transparent 70%);
    pointer-events: none;
}
.banner-icon { font-size: 3rem; flex-shrink: 0; }
.banner-title { font-size: 1.55rem; font-weight: 700; color: #e8f0fe; line-height: 1.2; }
.banner-subtitle {
    font-size: 0.8rem; color: #4a6a90; margin-top: 0.2rem;
    font-family: 'JetBrains Mono', monospace;
}
.banner-badges { display: flex; gap: 0.45rem; margin-top: 0.6rem; flex-wrap: wrap; }
.badge {
    background: #0f2040; border: 1px solid #1e3a60;
    color: #5a9ad0; font-size: 0.67rem; padding: 0.18rem 0.6rem;
    border-radius: 12px; font-family: 'JetBrains Mono', monospace;
}

/* Chat section title */
.chat-section-title {
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.14em; color: #2a4a6a; margin-bottom: 1.1rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.chat-section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(to right, #1a3050, transparent);
}

/* Welcome card */
.welcome-card {
    background: linear-gradient(135deg, #0c1829 0%, #091523 100%);
    border: 1px solid #142035; border-left: 3px solid #1a5fa0;
    border-radius: 14px; padding: 1.3rem 1.5rem; margin-bottom: 1.2rem;
}
.welcome-card h3 {
    color: #a8cef0 !important; font-size: 0.98rem !important;
    margin-bottom: 0.7rem !important;
}
.welcome-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 0.35rem 1.2rem; margin-top: 0.5rem;
}
.welcome-item {
    font-size: 0.82rem; color: #5a7a9a;
    display: flex; align-items: center; gap: 0.4rem; padding: 0.22rem 0;
}

/* User message */
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 1rem; }
.msg-user-bubble {
    background: linear-gradient(135deg, #1a4a8a 0%, #143a70 100%);
    border: 1px solid #2060a8; border-radius: 18px 18px 4px 18px;
    padding: 0.85rem 1.2rem; max-width: 72%; color: #d8eaf8;
    font-size: 0.91rem; line-height: 1.6;
    box-shadow: 0 4px 20px rgba(20,60,140,0.25);
}
.msg-user-meta { font-size: 0.69rem; color: #4a7ab0; margin-top: 0.35rem; text-align: right; }

/* Bot message */
.msg-bot { display: flex; justify-content: flex-start; margin-bottom: 0.4rem; }
.msg-bot-avatar {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #0f3060, #0a1f40);
    border: 1px solid #1a3a60; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0; margin-right: 0.7rem; margin-top: 0.1rem;
}
.msg-bot-content { max-width: 78%; }
.msg-bot-bubble {
    background: linear-gradient(135deg, #0d1e35 0%, #091627 100%);
    border: 1px solid #152a45; border-radius: 4px 18px 18px 18px;
    padding: 0.95rem 1.25rem; color: #c8ddf0;
    font-size: 0.9rem; line-height: 1.72;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.msg-bot-meta {
    font-size: 0.69rem; color: #2a4a6a; margin-top: 0.3rem;
    font-family: 'JetBrains Mono', monospace;
}

/* Chat input */
[data-testid="stChatInput"] {
    background: #0c1829 !important;
    border: 1.5px solid #1a3050 !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2a60a0 !important;
    box-shadow: 0 0 0 3px rgba(30,80,160,0.15) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #c8ddf0 !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.91rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #2a4060 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #2a60a0 !important; }

/* Animations */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1a2a40; border-radius: 4px; }

hr { border-color: #0f1e30 !important; margin: 0.6rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── TTS buttons — fully self-contained per iframe ─────────────────────────────
_TTS_STYLE = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; }
.tts-bar {
    display: flex; align-items: center; gap: 6px;
    padding: 5px 10px;
    background: #07101e;
    border: 1px solid #152535;
    border-radius: 9px;
    width: fit-content;
    font-family: 'Segoe UI', sans-serif;
}
.tts-bar button {
    background: #0f2040;
    border: 1px solid #1a3a60;
    color: #5a9ad0;
    font-size: 0.73rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    letter-spacing: 0.02em;
}
.tts-bar button:hover { background: #173050; color: #8ac8f0; }
.tts-bar button:active { background: #1e3f6a; }
.tts-lbl { font-size: 0.62rem; color: #2a4060; white-space: nowrap; letter-spacing: 0.05em; }
</style>
"""

def render_tts_buttons(text: str, msg_id: str, audio_b64: str = ""):
    """
    Render Speak / Pause / Stop controls for a bot message.

    Mode A — Coqui TTS (audio_b64 provided):
        A hidden <audio> element is embedded. Buttons call .play()/.pause()/.currentTime=0
        directly within the iframe.

    Mode B — Browser Web Speech API (no audio_b64):
        Uses window.top.speechSynthesis from inside the iframe.
    """
    safe_text = json.dumps(text)

    if audio_b64:
        html = _TTS_STYLE + f"""
        <audio id="aud{msg_id}" preload="auto">
            <source src="data:audio/wav;base64,{audio_b64}" type="audio/wav">
        </audio>
        <div class="tts-bar">
            <span class="tts-lbl">&#128266; TTS</span>
            <button onclick="document.getElementById('aud{msg_id}').play()">
                &#9654; Speak
            </button>
            <button onclick="document.getElementById('aud{msg_id}').pause()">
                &#9646;&#9646; Pause
            </button>
            <button onclick="(function(){{
                var a = document.getElementById('aud{msg_id}');
                a.pause(); a.currentTime = 0;
            }})()">
                &#9632; Stop
            </button>
        </div>
        """

    else:
        html = _TTS_STYLE + f"""
        <script>
        var _ss = (window.top || window).speechSynthesis;
        var _text = {safe_text};
        var _utt = null;

        function _tts_speak() {{
            if (!_ss) {{ alert('Speech synthesis not supported in this browser.'); return; }}
            _ss.cancel();
            _utt = new (window.top || window).SpeechSynthesisUtterance(_text);
            _utt.rate = 0.92;
            _utt.pitch = 1.0;

            var voices = _ss.getVoices();
            if (voices.length > 0) {{
                _apply_voice(_utt, voices);
                _ss.speak(_utt);
            }} else {{
                _ss.onvoiceschanged = function() {{
                    var v2 = _ss.getVoices();
                    _apply_voice(_utt, v2);
                    _ss.speak(_utt);
                    _ss.onvoiceschanged = null;
                }};
                setTimeout(function() {{
                    if (_ss && !_ss.speaking) {{ _ss.speak(_utt); }}
                }}, 300);
            }}
        }}

        function _apply_voice(utt, voices) {{
            var v = voices.find(function(v) {{ return v.lang === 'ur-PK'; }})
                 || voices.find(function(v) {{ return v.lang.startsWith('ur'); }})
                 || voices.find(function(v) {{ return v.lang === 'en-GB'; }})
                 || voices.find(function(v) {{ return v.lang.startsWith('en'); }});
            if (v) utt.voice = v;
        }}

        function _tts_pause() {{
            if (_ss && _ss.speaking) {{ _ss.pause(); }}
        }}

        function _tts_stop() {{
            if (_ss) {{ _ss.cancel(); }}
        }}
        </script>

        <div class="tts-bar">
            <span class="tts-lbl">&#128266; TTS</span>
            <button onclick="_tts_speak()">&#9654; Speak</button>
            <button onclick="_tts_pause()">&#9646;&#9646; Pause</button>
            <button onclick="_tts_stop()">&#9632; Stop</button>
        </div>
        """

    components.html(html, height=48, scrolling=False)


# ── Format AI markdown text to HTML ───────────────────────────────────────────
def fmt(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.*?)\*",     r"<em>\1</em>",          text)
    text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
    return text


# ── App class ─────────────────────────────────────────────────────────────────
class LegalChatApp:

    def __init__(self):
        self.init_session_state()
        self.agent = self.get_agent()
        self.db    = self.get_database()

    @staticmethod
    @st.cache_resource
    def get_agent():
        try:
            from TTS.api import TTS  # noqa: check if coqui-tts is available
            return LegalAgent(enable_tts=True)
        except ImportError:
            return LegalAgent(enable_tts=False)

    @staticmethod
    @st.cache_resource
    def get_database():
        return Database()

    def init_session_state(self):
        defaults = {
            'session_id':     str(uuid.uuid4()),
            'messages':       [],
            'language':       'english',
            'uploaded_files': [],
            'chat_started':   False,
            'tts_audio':      {},   # msg_index → audio_b64 (Coqui)
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v

        if not st.session_state.chat_started:
            self.get_agent().start_chat()
            st.session_state.chat_started = True

    # ── Sidebar helpers ────────────────────────────────────────────────────────
    def _section_label(self, icon: str, text: str):
        st.markdown(
            f'<div class="section-label-row">'
            f'<span class="section-label-icon">{icon}</span>'
            f'<span class="section-label-text">{text}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Sidebar ────────────────────────────────────────────────────────────────
    def render_sidebar(self):
        with st.sidebar:

            # Brand
            st.markdown(
                '<div class="sidebar-brand">'
                '<span class="sidebar-brand-icon">&#x2696;&#xFE0F;</span>'
                '<h1>PakJurist</h1>'
                '<p>Pakistan Legal Awareness System</p>'
                '</div>',
                unsafe_allow_html=True,
            )

            # Language
            self._section_label("&#x1F310;", "Language")
            lang = st.radio(
                "lang",
                ["English", "&#x627;&#x631;&#x62F;&#x648; (Urdu)", "Roman Urdu"],
                captions=None,
                index=0,
                label_visibility="collapsed",
            )
            if "Urdu" in lang and "Roman" not in lang:
                st.session_state.language = 'urdu'
            elif "Roman" in lang:
                st.session_state.language = 'roman'
            else:
                st.session_state.language = 'english'

            # Documents
            self._section_label("&#x1F4CE;", "Documents")
            uploaded = st.file_uploader(
                "Upload legal documents",
                type=['pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg'],
                label_visibility="collapsed",
            )
            if uploaded:
                self._process_file(uploaded)
            if st.session_state.uploaded_files:
                chips = "".join(
                    f'<span class="file-chip">&#x1F4C4; {f.name}</span>'
                    for f in st.session_state.uploaded_files
                )
                st.markdown(chips, unsafe_allow_html=True)
                if st.button("Clear uploads", use_container_width=True,
                             key="btn_clear_uploads"):
                    st.session_state.uploaded_files = []
                    st.session_state.pop('_last_upload', None)
                    st.rerun()

            # Voice Input
            self._section_label("&#x1F3A4;", "Voice Input")
            audio_bytes = audio_recorder(
                text="Click to record",
                recording_color="#1a5fa0",
                neutral_color="#2a4060",
                icon_name="microphone",
                icon_size="2x",
            )
            if audio_bytes and audio_bytes != st.session_state.get('_last_audio'):
                st.session_state['_last_audio'] = audio_bytes
                with st.spinner("Transcribing..."):
                    try:
                        t = self.agent.transcribe_audio(audio_bytes)
                        st.session_state.voice_input = t
                        st.success(f"Transcribed: {t[:50]}...")
                    except Exception as e:
                        st.error(str(e))

            # Topics
            self._section_label("&#x1F4DA;", "Quick Topics")
            for topic in self.agent.get_legal_topics():
                if st.button(topic, key=f"topic_{topic}",
                             use_container_width=True):
                    st.session_state.quick_question = (
                        f"Tell me about {topic} in Pakistan"
                    )

            # Session
            self._section_label("&#x2699;&#xFE0F;", "Session")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Clear chat", use_container_width=True,
                             key="btn_clear_chat"):
                    st.session_state.messages = []
                    st.session_state.tts_audio = {}
                    st.session_state.uploaded_files = []
                    self.db.clear_session(st.session_state.session_id)
                    self.agent.reset_chat()
                    st.rerun()
            with c2:
                if st.button("New session", use_container_width=True,
                             key="btn_new_session"):
                    st.session_state.session_id = str(uuid.uuid4())
                    st.session_state.messages = []
                    st.session_state.tts_audio = {}
                    st.session_state.uploaded_files = []
                    self.agent.reset_chat()
                    st.rerun()

            # Stats
            self._section_label("&#x1F4CA;", "Stats")
            stats = self.db.get_session_stats(st.session_state.session_id)
            if stats and stats.get('total_messages', 0) > 0:
                st.markdown(
                    f'<div class="stat-row"><span>Total messages</span>'
                    f'<span class="stat-value">{stats["total_messages"]}</span></div>'
                    f'<div class="stat-row"><span>Your questions</span>'
                    f'<span class="stat-value">{stats["user_messages"]}</span></div>'
                    f'<div class="stat-row"><span>Responses</span>'
                    f'<span class="stat-value">{stats["assistant_messages"]}</span></div>',
                    unsafe_allow_html=True,
                )

            # Disclaimer
            st.markdown(
                '<div class="disclaimer">'
                '<strong>&#x26A0;&#xFE0F; Disclaimer</strong><br>'
                'For educational purposes only. Not legal advice. '
                'Consult a licensed Pakistani lawyer for your specific matters.'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── File processing ────────────────────────────────────────────────────────
    def _process_file(self, f):
        if st.session_state.get('_last_upload') == f.name:
            return
        st.session_state['_last_upload'] = f.name
        with st.spinner("Processing document..."):
            try:
                if f.type == "application/pdf":
                    doc = self.agent.process_pdf(f)
                elif f.type in [
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "application/msword",
                ]:
                    doc = self.agent.process_docx(f)
                else:
                    doc = self.agent.process_image(f)
                st.session_state.uploaded_files.append(doc)
                st.success(f"Uploaded: {f.name}")
            except Exception as e:
                st.error(str(e))

    # ── Header ────────────────────────────────────────────────────────────────
    def render_header(self):
        st.markdown(
            '<div class="top-banner">'
            '<div class="banner-icon">&#x2696;&#xFE0F;</div>'
            '<div>'
            '<div class="banner-title">PakJurist</div>'
            '<div class="banner-subtitle">'
            'Pakistan Legal Awareness &amp; Constitutional Information Portal &nbsp;&middot;&nbsp; '
            '&#x646;&#x638;&#x627;&#x645; &#x642;&#x627;&#x646;&#x648;&#x646;&#x6CC; &#x622;&#x6AF;&#x627;&#x6C1;&#x6CC;'
            '</div>'
            '<div class="banner-badges">'
            '<span class="badge">Constitution of Pakistan</span>'
            '<span class="badge">PPC &middot; CrPC</span>'
            '<span class="badge">Family Law</span>'
            '<span class="badge">Commercial Law</span>'
            '<span class="badge">AI-Powered</span>'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── Chat area ─────────────────────────────────────────────────────────────
    def render_chat(self):
        st.markdown(
            '<div class="chat-section-title">&#x1F4AC; Conversation</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.messages:
            history = self.db.get_conversation_history(
                st.session_state.session_id, limit=50
            )
            st.session_state.messages = history

        if not st.session_state.messages:
            st.markdown(
                '<div class="welcome-card">'
                '<h3>&#x2696;&#xFE0F; Welcome to PakJurist</h3>'
                '<p style="color:#4a6a90;font-size:0.83rem;margin-bottom:0.7rem;">'
                'Your AI-powered Pakistan Legal Awareness companion. '
                'Ask any question about Pakistani law in English, Urdu, or Roman Urdu.</p>'
                '<div class="welcome-grid">'
                '<div class="welcome-item"><span>&#x1F4DC;</span><span>Constitution &amp; Articles</span></div>'
                '<div class="welcome-item"><span>&#x2696;&#xFE0F;</span><span>Criminal Law (PPC/CrPC)</span></div>'
                '<div class="welcome-item"><span>&#x1F4CB;</span><span>Civil &amp; Contract Law</span></div>'
                '<div class="welcome-item"><span>&#x1F46A;</span><span>Family &amp; Inheritance</span></div>'
                '<div class="welcome-item"><span>&#x1F4BC;</span><span>Business &amp; Commercial</span></div>'
                '<div class="welcome-item"><span>&#x1F3E2;</span><span>Administrative Law</span></div>'
                '<div class="welcome-item"><span>&#x1F3A4;</span><span>Voice Input</span></div>'
                '<div class="welcome-item"><span>&#x1F50A;</span><span>TTS Voice Output</span></div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="chat-section-title" style="margin-top:0.8rem;">'
                '&#x1F4A1; Quick Questions</div>',
                unsafe_allow_html=True,
            )
            qs = self.agent.get_quick_questions()
            cols = st.columns(3)
            for i, q in enumerate(qs):
                with cols[i % 3]:
                    if st.button(q, key=f"qq_{i}", use_container_width=True):
                        st.session_state.quick_question = q
                        st.rerun()

        for idx, msg in enumerate(st.session_state.messages):
            role    = msg['role']
            content = msg['content']
            ts      = msg.get('timestamp', '')

            if role == 'user':
                st.markdown(
                    f'<div class="msg-user">'
                    f'<div class="msg-user-bubble">'
                    f'{content}'
                    f'<div class="msg-user-meta">&#x1F550; {ts}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="msg-bot">'
                    f'<div class="msg-bot-avatar">&#x2696;&#xFE0F;</div>'
                    f'<div class="msg-bot-content">'
                    f'<div class="msg-bot-bubble">{fmt(content)}</div>'
                    f'<div class="msg-bot-meta">'
                    f'PakJurist &nbsp;&middot;&nbsp; &#x1F550; {ts}'
                    f'</div></div></div>',
                    unsafe_allow_html=True,
                )
                audio_b64 = st.session_state.tts_audio.get(idx, "")
                render_tts_buttons(content, str(idx), audio_b64)

    # ── Input handling ────────────────────────────────────────────────────────
    def handle_input(self):
        user_input = None
        if 'quick_question' in st.session_state:
            user_input = st.session_state.pop('quick_question')
        elif 'voice_input' in st.session_state:
            user_input = st.session_state.pop('voice_input')
        else:
            user_input = st.chat_input(
                "Ask PakJurist about Pakistani laws, constitution, legal procedures..."
            )
        return user_input

    def process_message(self, user_input: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        display = user_input
        if "[USER QUESTION]:" in user_input:
            display = user_input.split("[USER QUESTION]: ")[-1]

        st.session_state.messages.append(
            {'role': 'user', 'content': display, 'timestamp': ts}
        )
        self.db.save_message(st.session_state.session_id, 'user', display)

        with st.spinner("PakJurist is analysing legal information..."):
            try:
                result = self.agent.generate_response_with_audio(
                    user_message=user_input,
                    language=st.session_state.language,
                    documents=st.session_state.uploaded_files or None,
                )
                response_text = result["text"]
                tts_result    = result["tts"]

                bot_idx = len(st.session_state.messages)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response_text, 'timestamp': ts}
                )
                self.db.save_message(
                    st.session_state.session_id, 'assistant', response_text
                )

                if tts_result and getattr(tts_result, 'audio_b64', None):
                    st.session_state.tts_audio[bot_idx] = tts_result.audio_b64

                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Please try again in a moment.")

    # ── Run ───────────────────────────────────────────────────────────────────
    def run(self):
        self.render_sidebar()
        self.render_header()
        self.render_chat()
        user_input = self.handle_input()
        if user_input:
            self.process_message(user_input)


def main():
    app = LegalChatApp()
    app.run()


if __name__ == "__main__":
    main()