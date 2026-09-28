import streamlit as st
import os
import time
from src.pdf_loader import load_pdf
from src.text_splitter import split_into_chunks
from src.vector_store import build_vector_store, build_hybrid_retriever
from src.config import Config
from src.logger import get_logger
from ui.styles import get_theme

logger = get_logger(__name__)


def reset_quiz():
    defaults = {
        "quiz_questions": None, "quiz_index": 0, "quiz_score": 0,
        "quiz_answered": False, "quiz_selected": None, "quiz_complete": False
    }
    for k, v in defaults.items():
        st.session_state[k] = v


def render_sidebar():
    T = get_theme()
    with st.sidebar:

        # ── Brand ─────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="brand-wrap">
            <div class="brand-logo">
                <div class="brand-icon">📄</div>
                <div class="brand-name">Chat With PDF</div>
            </div>
            <div class="brand-tagline">RAG · Document Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Document upload ────────────────────────────────────────────────
        st.markdown('<div class="nav-label">Document</div>',
                    unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload PDF", type=["pdf"],
            label_visibility="collapsed"
        )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        if uploaded_file is not None:
            st.caption(f"📎 {uploaded_file.name}")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

            if st.button("⚡ Process Document", use_container_width=True):
                progress = st.progress(0, text="📤 Uploading...")
                try:
                    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
                    save_path = os.path.join(Config.UPLOAD_DIR, uploaded_file.name)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    progress.progress(0.3, text="📖 Extracting text...")
                    pages = load_pdf(save_path)

                    progress.progress(0.5, text="✂️ Chunking...")
                    chunks = split_into_chunks(pages)

                    progress.progress(0.75, text="🧠 Embedding...")
                    vector_store = build_vector_store(chunks)

                    progress.progress(0.9, text="🔍 Building index...")
                    retriever = build_hybrid_retriever(vector_store, chunks)

                    st.session_state.retriever     = retriever
                    st.session_state.all_chunks    = chunks
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.total_pages   = len(pages)
                    st.session_state.chat_history  = []
                    st.session_state.active_view   = "chat"
                    reset_quiz()

                    time.sleep(0.4)
                    progress.progress(1.0, text="✅ Ready!")
                    time.sleep(0.5)
                    progress.empty()
                    st.success(f"✅ {len(chunks)} chunks · {len(pages)} pages")

                except Exception as e:
                    progress.empty()
                    logger.error(f"Processing error: {e}")
                    st.error(f"Error: {e}")

        # ── Doc info card ──────────────────────────────────────────────────
        if st.session_state.get("document_name"):
            name = st.session_state.document_name
            display = name if len(name) <= 22 else name[:19] + "..."
            st.markdown(f"""
            <div class="doc-card">
                <div class="doc-card-name">📄 {display}</div>
                <div class="doc-meta-grid">
                    <div class="doc-meta-item">
                        <span class="doc-meta-label">Pages</span>
                        <span class="doc-meta-value">
                            {st.session_state.get('total_pages', '—')}
                        </span>
                    </div>
                    <div class="doc-meta-item">
                        <span class="doc-meta-label">Chunks</span>
                        <span class="doc-meta-value">
                            {len(st.session_state.get('all_chunks', []))}
                        </span>
                    </div>
                    <div class="doc-meta-item">
                        <span class="doc-meta-label">Embeddings</span>
                        <span class="doc-meta-value">MiniLM</span>
                    </div>
                    <div class="doc-meta-item">
                        <span class="doc-meta-label">LLM</span>
                        <span class="doc-meta-value">Gemini 2.5</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Mode selector ──────────────────────────────────────────────────
        if st.session_state.get("retriever") is not None:
            st.markdown('<div class="nav-label">Mode</div>',
                        unsafe_allow_html=True)
            st.radio(
                "Mode",
                label_visibility="collapsed",
                options=[
                    "🔹 Ask Document",
                    "🔹 Summarize PDF",
                    "🔹 Extract Key Points",
                    "🎓 Explain Like Beginner",
                    "🎮 Quiz Game",
                ],
                index=0,
                key="mode"
            )

        # ── Chat history ───────────────────────────────────────────────────
        user_msgs = [
            m["content"] for m in st.session_state.get("chat_history", [])
            if m["role"] == "user"
        ]
        if user_msgs:
            st.markdown('<div class="nav-label">Recent</div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="history-wrap">', unsafe_allow_html=True)
            for msg in reversed(user_msgs[-4:]):
                preview = msg if len(msg) <= 34 else msg[:31] + "..."
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-dot"></div>
                    <span>{preview}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                reset_quiz()
                st.rerun()

        # ── Footer ─────────────────────────────────────────────────────────
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<hr style="border-color:{T["border"]}; margin:0 0 12px">',
            unsafe_allow_html=True
        )

        # Settings + Help row
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            is_settings = st.session_state.active_view == "settings"
            if st.button(
                "⚙️ Settings",
                use_container_width=True,
                type="primary" if is_settings else "secondary",
                key="btn_settings"
            ):
                st.session_state.active_view = (
                    "chat" if is_settings else "settings"
                )
                st.rerun()
        with btn_col2:
            is_help = st.session_state.active_view == "help"
            if st.button(
                "❓ Help",
                use_container_width=True,
                type="primary" if is_help else "secondary",
                key="btn_help"
            ):
                st.session_state.active_view = (
                    "chat" if is_help else "help"
                )
                st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Theme toggle row
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button(
                "🌙 Dark",
                use_container_width=True,
                type="primary" if st.session_state.theme == "dark" else "secondary",
                key="btn_dark"
            ):
                st.session_state.theme = "dark"
                st.rerun()
        with theme_col2:
            if st.button(
                "☀️ Light",
                use_container_width=True,
                type="primary" if st.session_state.theme == "light" else "secondary",
                key="btn_light"
            ):
                st.session_state.theme = "light"
                st.rerun()

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)