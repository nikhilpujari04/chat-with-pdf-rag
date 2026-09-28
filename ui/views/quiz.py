import streamlit as st
from src.rag_chain import generate_quiz
from ui.styles import get_theme
from src.logger import get_logger

logger = get_logger(__name__)


def reset_quiz():
    st.session_state.quiz_questions = None
    st.session_state.quiz_index     = 0
    st.session_state.quiz_score     = 0
    st.session_state.quiz_answered  = False
    st.session_state.quiz_selected  = None
    st.session_state.quiz_complete  = False


def render_quiz():
    T = get_theme()
    st.markdown("## 🎮 Quiz Game")

    # ── Not started yet ───────────────────────────────────────────────────────
    if st.session_state.quiz_questions is None:
        st.markdown(
            f'<p style="color:{T["text_muted"]}">Test your knowledge with an '
            f'AI-generated quiz based on your document.</p>',
            unsafe_allow_html=True
        )
        if st.button("🚀 Start Quiz"):
            with st.spinner("Generating quiz..."):
                result = generate_quiz(st.session_state.all_chunks)
                if result["error"]:
                    st.error(result["error"])
                else:
                    reset_quiz()
                    st.session_state.quiz_questions = result["questions"]
                    st.rerun()

    # ── Results screen ────────────────────────────────────────────────────────
    elif st.session_state.quiz_complete:
        total = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        pct   = score / total

        if pct == 1.0:   grade, emoji = "Perfect Score!", "🥇"
        elif pct >= 0.8: grade, emoji = "Excellent!",     "🥈"
        elif pct >= 0.6: grade, emoji = "Good Job!",      "🥉"
        else:            grade, emoji = "Keep Practicing!","📚"

        st.markdown(f"""
        <div class="result-card">
            <div style="font-size:3.5rem">{emoji}</div>
            <div style="font-size:1.8rem; font-weight:800;
                 color:{T['text_head']}; margin:12px 0">{grade}</div>
            <div style="color:{T['text_muted']}; margin-bottom:8px">
                You scored</div>
            <div style="font-size:3.5rem; font-weight:900;
                 background:linear-gradient(135deg,#06B6D4,#22D3EE);
                 -webkit-background-clip:text;
                 -webkit-text-fill-color:transparent">
                {score}/{total}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Try Again"):
            reset_quiz()
            st.rerun()

    # ── Active question ───────────────────────────────────────────────────────
    else:
        questions = st.session_state.quiz_questions
        idx   = st.session_state.quiz_index
        total = len(questions)
        q     = questions[idx]

        st.markdown(f"""
        <div class="score-badge">
            Question {idx+1} of {total}
            &nbsp;|&nbsp;
            Score: {st.session_state.quiz_score}/{total}
        </div>
        """, unsafe_allow_html=True)

        st.progress(idx / total)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="quiz-card">
            <div class="quiz-question">Q{idx+1}. {q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.quiz_answered:
            cols = st.columns(2)
            for i, opt in enumerate(q["options"]):
                with cols[i % 2]:
                    if st.button(
                        f"{chr(65+i)}. {opt}",
                        key=f"opt_{idx}_{i}",
                        use_container_width=True
                    ):
                        st.session_state.quiz_answered = True
                        st.session_state.quiz_selected = i
                        if i == q["correct_index"]:
                            st.session_state.quiz_score += 1
                        st.rerun()
        else:
            selected = st.session_state.quiz_selected
            correct  = q["correct_index"]

            for i, opt in enumerate(q["options"]):
                label = f"{chr(65+i)}. {opt}"
                if i == correct:
                    st.markdown(
                        f'<div class="correct-answer">✅ {label}</div>',
                        unsafe_allow_html=True
                    )
                elif i == selected and selected != correct:
                    st.markdown(
                        f'<div class="wrong-answer">❌ {label}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div style="padding:8px;color:{T["text_muted"]}">'
                        f'{label}</div>',
                        unsafe_allow_html=True
                    )

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            is_last = (idx == total - 1)
            if st.button("🏁 See Results" if is_last else "Next Question →"):
                if is_last:
                    st.session_state.quiz_complete = True
                else:
                    st.session_state.quiz_index   += 1
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                st.rerun()