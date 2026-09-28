import streamlit as st
from src.rag_chain import summarize_document, extract_key_points
from src.logger import get_logger

logger = get_logger(__name__)


def render_document():
    mode = st.session_state.get("mode", "🔹 Summarize PDF")
    label = mode.replace("🔹 ", "")
    st.markdown(f"## 📝 {label}")

    if st.button(f"▶ Run {label}"):
        with st.spinner(f"Running {label}..."):
            try:
                result = (
                    summarize_document(st.session_state.all_chunks)
                    if mode == "🔹 Summarize PDF"
                    else extract_key_points(st.session_state.all_chunks)
                )
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": []
                })
                st.rerun()
            except Exception as e:
                logger.error(f"Document mode error: {e}")
                st.error(f"Error: {e}")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])