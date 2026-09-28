import streamlit as st


def render_settings():
    st.markdown("## ⚙️ Settings")
    st.caption(
        "Retrieval and LLM settings apply immediately. "
        "Chunk settings require re-processing your document."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">🔍 Retrieval</div>',
                    unsafe_allow_html=True)
        st.session_state.setting_k = st.slider(
            "Top-K chunks", 3, 12,
            st.session_state.setting_k,
            help="More chunks = broader context. Start at 6."
        )
        st.session_state.setting_bm25_weight = st.slider(
            "BM25 (keyword) weight", 0.0, 1.0,
            st.session_state.setting_bm25_weight, 0.05,
            help="0.5 = equal keyword + semantic search."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-section-title">🤖 LLM</div>',
                    unsafe_allow_html=True)
        st.session_state.setting_temperature = st.slider(
            "Temperature", 0.0, 1.0,
            st.session_state.setting_temperature, 0.05,
            help="Lower = more factual. Higher = more creative."
        )
        st.selectbox(
            "Model",
            ["gemini-2.5-flash", "gemini-2.5-pro"],
            help="Pro is more capable but uses more API quota."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-section-title">'
        '✂️ Chunking (requires re-processing)'
        '</div>',
        unsafe_allow_html=True
    )
    st.warning(
        "⚠️ Changing chunk settings only takes effect after "
        "re-uploading and re-processing your document."
    )
    col3, col4 = st.columns(2)
    with col3:
        st.session_state.setting_chunk_size = st.slider(
            "Chunk size (chars)", 300, 1500,
            st.session_state.setting_chunk_size, 50,
            help="Smaller = more precise. Larger = more context per chunk."
        )
    with col4:
        st.session_state.setting_chunk_overlap = st.slider(
            "Overlap (chars)", 50, 300,
            st.session_state.setting_chunk_overlap, 10,
            help="Prevents ideas from being cut off at chunk boundaries."
        )
    st.markdown('</div>', unsafe_allow_html=True)