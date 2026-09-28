import streamlit as st
from src.rag_chain import query_documents, explain_like_beginner
from src.logger import get_logger
from ui.styles import get_theme

logger = get_logger(__name__)


def render_chat():
    T = get_theme()
    mode = st.session_state.get("mode", "🔹 Ask Document")

    title = "💬 Ask Document" if mode == "🔹 Ask Document" \
            else "🎓 Explain Like Beginner"
    st.markdown(f"## {title}")

    # Redraw history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                citation = " · ".join([f"📄 Page {p}" for p in msg["sources"]])
                st.markdown(
                    f'<div class="source-citation">'
                    f'<strong style="color:{T["accent"]}">Sources</strong>'
                    f' · {citation}</div>',
                    unsafe_allow_html=True
                )

    placeholder = (
        "Ask anything about your PDF..."
        if mode == "🔹 Ask Document"
        else "What would you like explained in simple terms?"
    )

    if question := st.chat_input(placeholder):
        st.session_state.chat_history.append({
            "role": "user", "content": question
        })
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = (
                        query_documents(st.session_state.retriever, question)
                        if mode == "🔹 Ask Document"
                        else explain_like_beginner(
                            st.session_state.retriever, question
                        )
                    )
                    st.write(result["answer"])

                    if result["sources"]:
                        citation = " · ".join(
                            [f"📄 Page {p}" for p in result["sources"]]
                        )
                        st.markdown(
                            f'<div class="source-citation">'
                            f'<strong style="color:{T["accent"]}">Sources</strong>'
                            f' · {citation}</div>',
                            unsafe_allow_html=True
                        )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"]
                    })
                except Exception as e:
                    logger.error(f"Chat error: {e}")
                    st.error(f"Something went wrong: {e}")