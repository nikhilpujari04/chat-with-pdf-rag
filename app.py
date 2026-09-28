"""
Chat With PDF — RAG-based Document Intelligence System
Entry point: initializes session state, injects styles, renders sidebar + view.
"""

import streamlit as st
from ui.styles import inject_styles
from ui.sidebar import render_sidebar
from ui.views.welcome import render_welcome
from ui.views.chat import render_chat
from ui.views.document import render_document
from ui.views.quiz import render_quiz
from ui.views.settings import render_settings
from ui.views.help import render_help

st.set_page_config(
    page_title="Chat With PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state defaults ────────────────────────────────────────────────────
DEFAULTS = {
    "retriever":              None,
    "all_chunks":             [],
    "chat_history":           [],
    "document_name":          None,
    "total_pages":            0,
    "active_view":            "chat",
    "theme":                  "dark",
    "mode":                   "🔹 Ask Document",
    "quiz_questions":         None,
    "quiz_index":             0,
    "quiz_score":             0,
    "quiz_answered":          False,
    "quiz_selected":          None,
    "quiz_complete":          False,
    "setting_k":              6,
    "setting_temperature":    0.3,
    "setting_bm25_weight":    0.5,
    "setting_chunk_size":     600,
    "setting_chunk_overlap":  100,
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Inject theme + particles ──────────────────────────────────────────────────
inject_styles()

# ── Sidebar ───────────────────────────────────────────────────────────────────
render_sidebar()

# ── Main view routing ─────────────────────────────────────────────────────────
view   = st.session_state.active_view
mode   = st.session_state.get("mode", "🔹 Ask Document")
has_doc = st.session_state.retriever is not None

if view == "settings":
    render_settings()
elif view == "help":
    render_help()
elif not has_doc:
    render_welcome()
elif mode == "🎮 Quiz Game":
    render_quiz()
elif mode in ["🔹 Summarize PDF", "🔹 Extract Key Points"]:
    render_document()
else:
    render_chat()