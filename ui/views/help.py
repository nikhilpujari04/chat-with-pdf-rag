import streamlit as st
from ui.styles import get_theme


def render_help():
    T = get_theme()
    st.markdown("## ❓ Help & Documentation")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">🚀 How to use</div>',
                    unsafe_allow_html=True)
        st.markdown("""
1. **Upload a PDF** using the sidebar uploader
2. Click **⚡ Process Document**
3. Wait for all processing steps to complete
4. **Pick a mode** and start chatting
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">🎯 Modes explained</div>',
                    unsafe_allow_html=True)
        st.markdown("""
| Mode | What it does |
|------|-------------|
| 💬 Ask Document | Specific Q&A with cited sources |
| 📝 Summarize PDF | Concise document summary |
| 🔑 Extract Key Points | Bullet-point fact extraction |
| 🎓 Explain Like Beginner | Plain-language simplification |
| 🎮 Quiz Game | Interactive 5-question quiz with scoring |
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">⚙️ How RAG works</div>',
                    unsafe_allow_html=True)
        st.markdown("""
1. PDF split into overlapping text chunks
2. Each chunk embedded as a semantic vector
3. Vectors indexed in FAISS for fast search
4. Your question retrieves the top matching chunks
   using **hybrid search** (semantic + keyword)
5. Chunks passed to Gemini as grounded context
6. Gemini answers based **only** on that context
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">⚠️ Known limitations</div>',
                    unsafe_allow_html=True)
        limitations = [
            ("🖼️", "Scanned / image-based PDFs not supported (no OCR)"),
            ("📏", "Very large docs may truncate in summary modes"),
            ("🔤", "Retrieval depends on phrasing — rephrase if answer seems wrong"),
            ("🎨", "Designed PDF templates (Canva etc.) may extract with spacing issues"),
            ("🌐", "Requires internet for Gemini API calls"),
        ]
        for icon, text in limitations:
            st.markdown(
                f'<div class="limitation-item">'
                f'<span>{icon}</span><span>{text}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)