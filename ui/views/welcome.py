import streamlit as st
from ui.styles import get_theme


def render_welcome():
    T = get_theme()
    st.markdown(
        '<div class="brand-name" style="font-size:2.2rem; margin-bottom:6px">'
        '📄 Chat With PDF</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<p style="color:{T["text_muted"]}; font-size:1rem; margin-bottom:28px">'
        'RAG-based Document Intelligence — upload a PDF to get started</p>',
        unsafe_allow_html=True
    )

    features = [
        ("💬", "Ask Document",
         "Ask any question and get grounded, cited answers from your PDF"),
        ("📝", "Summarize PDF",
         "Generate a concise, accurate summary in seconds"),
        ("🔑", "Extract Key Points",
         "Pull out the most important facts as a clean bullet list"),
        ("🎓", "Explain Like Beginner",
         "Get complex topics broken down in plain, simple language"),
        ("🎮", "Quiz Game",
         "Turn your document into an interactive quiz and earn points"),
    ]

    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="welcome-feature">
                <div style="font-size:1.6rem; margin-bottom:6px">{icon}</div>
                <div style="font-weight:700; color:{T['text_head']};
                     margin-bottom:4px">{title}</div>
                <div style="font-size:0.85rem; color:{T['text_muted']}">{desc}</div>
            </div>
            """, unsafe_allow_html=True)