import streamlit as st


def get_theme():
    if st.session_state.get("theme", "dark") == "light":
        return {
            "bg_main":      "#F8FAFF",
            "bg_sidebar":   "#F0F4FF",
            "bg_card":      "#FFFFFF",
            "bg_card2":     "#F5F8FF",
            "border":       "#E2E8F0",
            "border_hover": "#06B6D4",
            "text_main":    "#0F172A",
            "text_secondary":"#475569",
            "text_muted":   "#94A3B8",
            "text_head":    "#0C1929",
            "accent":       "#0891B2",
            "accent_light": "#06B6D4",
            "accent_glow":  "rgba(8,145,178,0.15)",
            "accent_subtle":"rgba(8,145,178,0.08)",
            "user_msg_bg":  "linear-gradient(135deg,#0E7490,#0891B2)",
            "ai_msg_bg":    "#FFFFFF",
        }
    return {
        "bg_main":      "#0A0A0F",
        "bg_sidebar":   "#0D0D14",
        "bg_card":      "#13131A",
        "bg_card2":     "#16161F",
        "border":       "#1E1E2E",
        "border_hover": "#06B6D4",
        "text_main":    "#E2E8F0",
        "text_secondary":"#94A3B8",
        "text_muted":   "#4A5568",
        "text_head":    "#F8FAFC",
        "accent":       "#06B6D4",
        "accent_light": "#22D3EE",
        "accent_glow":  "rgba(6,182,212,0.15)",
        "accent_subtle":"rgba(6,182,212,0.06)",
        "user_msg_bg":  "linear-gradient(135deg,#0C4A6E,#0E7490)",
        "ai_msg_bg":    "#13131A",
    }


def inject_styles():
    T = get_theme()
    is_dark = st.session_state.get("theme", "dark") == "dark"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700;0,14..32,800&display=swap');

/* ── Reset & base ──────────────────────────────────────────────────────────── */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body, button, input, textarea, select, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', -apple-system, sans-serif;
}}

.material-icons,
.material-icons-outlined,
.material-icons-rounded,
.material-icons-sharp,
.material-icons-two-tone,
.stIconMaterial,
[class*="material-icons"] {{
    font-family: 'Material Icons', 'Material Symbols Outlined', sans-serif !important;
}}

[data-testid="stAppViewContainer"] {{
    background: {T['bg_main']} !important;
    color: {T['text_main']};
    font-size: 15px;
    line-height: 1.65;
}}

/* Remove Streamlit's default padding */
.main .block-container {{
    padding: 24px 32px 80px !important;
    max-width: 860px !important;
    margin: 0 auto !important;
}}

/* ── Sidebar ───────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {T['bg_sidebar']} !important;
    border-right: 1px solid {T['border']} !important;
    width: 260px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 0 !important;
}}

/* ── Typography ────────────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5 {{
    color: {T['text_head']} !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.3 !important;
}}
p, li, span, div {{
    color: {T['text_main']};
}}
.text-muted {{
    color: {T['text_muted']} !important;
    font-size: 0.82rem !important;
}}
.text-secondary {{
    color: {T['text_secondary']} !important;
}}

/* ── Particle canvas ───────────────────────────────────────────────────────── */
#cwp-bg {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
    opacity: 1;
}}
[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}
[data-testid="stSidebar"] {{
    position: relative;
    z-index: 2;
}}

/* ── Keyframes ─────────────────────────────────────────────────────────────── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
@keyframes gradFlow {{
    0%   {{ background-position: 0% 50%; }}
    50%  {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
@keyframes softPulse {{
    0%, 100% {{ opacity: 0.7; }}
    50%       {{ opacity: 1; }}
}}
@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(12px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-12px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}
@keyframes countUp {{
    from {{ transform: scale(0.8); opacity: 0; }}
    to   {{ transform: scale(1); opacity: 1; }}
}}

/* ── Brand / logo ──────────────────────────────────────────────────────────── */
.brand-wrap {{
    padding: 20px 18px 16px;
    border-bottom: 1px solid {T['border']};
}}
.brand-logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2px;
}}
.brand-icon {{
    width: 32px; height: 32px;
    background: linear-gradient(135deg, {T['accent']}, {T['accent_light']});
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    box-shadow: 0 0 12px {T['accent_glow']};
}}
.brand-name {{
    background: linear-gradient(135deg, {T['accent_light']}, #67E8F9, {T['accent']});
    background-size: 200% 200%;
    animation: gradFlow 4s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
}}
.brand-tagline {{
    color: {T['text_muted']};
    font-size: 0.7rem;
    letter-spacing: 0.04em;
    padding-left: 42px;
}}

/* ── Sidebar nav section label ─────────────────────────────────────────────── */
.nav-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {T['text_muted']};
    padding: 14px 18px 6px;
}}

/* ── Doc info card ─────────────────────────────────────────────────────────── */
.doc-card {{
    margin: 10px 14px;
    padding: 12px 14px;
    background: {T['bg_card2']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    animation: fadeUp 0.35s ease forwards;
}}
.doc-card-name {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {T['text_head']};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid {T['border']};
}}
.doc-meta-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
}}
.doc-meta-item {{
    display: flex;
    flex-direction: column;
}}
.doc-meta-label {{
    font-size: 0.65rem;
    color: {T['text_muted']};
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}
.doc-meta-value {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {T['accent']};
}}

/* ── Chat history items ────────────────────────────────────────────────────── */
.history-wrap {{
    padding: 0 14px;
}}
.history-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 7px 10px;
    border-radius: 7px;
    margin-bottom: 2px;
    font-size: 0.8rem;
    color: {T['text_secondary']};
    cursor: default;
    transition: all 0.18s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    border: 1px solid transparent;
}}
.history-item:hover {{
    background: {T['accent_subtle']};
    color: {T['accent_light']};
    border-color: {T['border']};
}}
.history-dot {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {T['accent']};
    flex-shrink: 0;
    animation: softPulse 2s ease infinite;
}}

/* ── Nav buttons (Settings / Help / Theme) ─────────────────────────────────── */
.nav-footer {{
    position: sticky;
    bottom: 0;
    background: {T['bg_sidebar']};
    border-top: 1px solid {T['border']};
    padding: 12px 14px;
}}

/* ── Main chat messages ────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {{
    display: flex !important;
    align-items: flex-start !important;
    gap: 14px !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin-bottom: 10px !important;
    border: 1px solid {T['border']} !important;
}}
[data-testid="stChatMessage"] > div:first-child {{
    flex-shrink: 0 !important;
}}
[data-testid="stChatMessage"] > div:not(:first-child) {{
    flex: 1 1 auto !important;
    min-width: 0 !important;
}}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
    background: {T['user_msg_bg']} !important;
    border-color: rgba(6,182,212,0.3) !important;
    animation: slideInRight 0.3s ease forwards;
}}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
    background: {T['ai_msg_bg']} !important;
    animation: slideInLeft 0.3s ease forwards;
}}

/* ── Source citation tag ───────────────────────────────────────────────────── */
.citation-wrap {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 10px;
}}
.citation-tag {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 3px 10px;
    background: {T['accent_subtle']};
    border: 1px solid {T['border_hover']};
    border-radius: 20px;
    font-size: 0.75rem;
    color: {T['accent_light']};
    font-weight: 500;
}}

/* ── Buttons ───────────────────────────────────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent_light']}) !important;
    color: {'#000000' if is_dark else '#FFFFFF'} !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    padding: 8px 18px !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 8px {T['accent_glow']} !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px {T['accent_glow']} !important;
    opacity: 0.92 !important;
}}
.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* Secondary buttons */
button[kind="secondary"] {{
    background: {T['bg_card2']} !important;
    color: {T['text_secondary']} !important;
    border: 1px solid {T['border']} !important;
    box-shadow: none !important;
}}
button[kind="secondary"]:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
}}

/* ── File uploader ─────────────────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {{
    background: {T['bg_card2']} !important;
    border: 1px dashed {T['border']} !important;
    border-radius: 10px !important;
    transition: border-color 0.2s ease !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: {T['accent']} !important;
}}
[data-testid="stFileUploaderDropzone"] button {{
    background: linear-gradient(135deg,{T['accent']},{T['accent_light']}) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    min-width: 110px !important;
}}
[data-testid="stFileUploaderDropzone"] button::before,
[data-testid="stFileUploaderDropzone"] button::after {{
    content: none !important;
}}

/* ── Quiz ──────────────────────────────────────────────────────────────────── */
.quiz-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 14px 18px;
    background: {T['bg_card']};
    border: 1px solid {T['border']};
    border-radius: 10px;
}}
.quiz-counter {{
    font-size: 0.82rem;
    color: {T['text_muted']};
    font-weight: 500;
}}
.quiz-score {{
    font-size: 0.88rem;
    font-weight: 700;
    color: {T['accent']};
}}
.quiz-question-card {{
    padding: 22px 24px;
    background: {T['bg_card']};
    border: 1px solid {T['border']};
    border-left: 3px solid {T['accent']};
    border-radius: 10px;
    margin-bottom: 18px;
    animation: fadeUp 0.3s ease forwards;
}}
.quiz-q-text {{
    font-size: 1rem;
    font-weight: 600;
    color: {T['text_head']};
    line-height: 1.5;
}}
.opt-correct {{
    padding: 11px 16px;
    background: rgba(22,163,74,0.12);
    border: 1px solid #16A34A;
    border-radius: 8px;
    color: #4ADE80;
    font-size: 0.9rem;
    margin-bottom: 6px;
    animation: fadeIn 0.25s ease forwards;
}}
.opt-wrong {{
    padding: 11px 16px;
    background: rgba(220,38,38,0.1);
    border: 1px solid #DC2626;
    border-radius: 8px;
    color: #F87171;
    font-size: 0.9rem;
    margin-bottom: 6px;
    animation: fadeIn 0.25s ease forwards;
}}
.opt-neutral {{
    padding: 11px 16px;
    background: transparent;
    border: 1px solid {T['border']};
    border-radius: 8px;
    color: {T['text_muted']};
    font-size: 0.9rem;
    margin-bottom: 6px;
}}
.result-wrap {{
    text-align: center;
    padding: 48px 32px;
    background: {T['bg_card']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    animation: fadeUp 0.5s ease forwards;
}}
.result-emoji {{
    font-size: 4rem;
    margin-bottom: 12px;
    animation: countUp 0.5s ease forwards;
}}
.result-grade {{
    font-size: 1.6rem;
    font-weight: 800;
    color: {T['text_head']};
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}}
.result-score {{
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, {T['accent']}, {T['accent_light']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    animation: countUp 0.6s ease 0.1s both;
}}
.result-label {{
    font-size: 0.85rem;
    color: {T['text_muted']};
    margin-bottom: 6px;
}}

/* ── Panel cards (settings / help) ─────────────────────────────────────────── */
.panel-card {{
    background: {T['bg_card']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
    animation: fadeUp 0.35s ease forwards;
}}
.panel-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {T['accent']};
    margin-bottom: 14px;
    display: block;
}}

/* ── Welcome screen ────────────────────────────────────────────────────────── */
.welcome-hero {{
    margin-bottom: 32px;
    animation: fadeUp 0.4s ease forwards;
}}
.welcome-title {{
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, {T['text_head']}, {T['accent_light']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    margin-bottom: 10px;
}}
.welcome-sub {{
    font-size: 1rem;
    color: {T['text_secondary']};
    max-width: 480px;
}}
.feature-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 28px;
}}
.feature-card {{
    padding: 18px;
    background: {T['bg_card']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    transition: all 0.2s ease;
    animation: fadeUp 0.4s ease forwards;
    cursor: default;
}}
.feature-card:hover {{
    border-color: {T['accent']};
    transform: translateY(-2px);
    box-shadow: 0 6px 20px {T['accent_glow']};
}}
.feature-icon {{
    font-size: 1.4rem;
    margin-bottom: 8px;
}}
.feature-title {{
    font-size: 0.9rem;
    font-weight: 700;
    color: {T['text_head']};
    margin-bottom: 4px;
}}
.feature-desc {{
    font-size: 0.78rem;
    color: {T['text_muted']};
    line-height: 1.5;
}}

/* ── Progress bar ──────────────────────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {{
    background: linear-gradient(90deg, {T['accent']}, {T['accent_light']}) !important;
    border-radius: 4px !important;
}}

/* ── Inputs / sliders ──────────────────────────────────────────────────────── */
[data-testid="stSlider"] [data-testid="stThumbValue"] {{
    color: {T['accent']} !important;
}}

/* ── Divider ───────────────────────────────────────────────────────────────── */
hr {{
    border-color: {T['border']} !important;
    margin: 10px 0 !important;
}}

/* ── Scrollbar ─────────────────────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: {T['border']};
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {T['accent']};
}}

/* ── Limitation items ──────────────────────────────────────────────────────── */
.limit-item {{
    display: flex;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid {T['border']};
    font-size: 0.85rem;
    color: {T['text_secondary']};
}}
.limit-item:last-child {{ border-bottom: none; }}
</style>

<canvas id="cwp-bg"></canvas>

<script>
(function() {{
    function boot() {{
        const c = document.getElementById('cwp-bg');
        if (!c) {{ setTimeout(boot, 200); return; }}
        const ctx = c.getContext('2d');

        function resize() {{
            c.width  = window.innerWidth;
            c.height = window.innerHeight;
        }}
        resize();
        window.addEventListener('resize', resize);

        const N = 28;
        const bs = [];
        const isDark = {'true' if is_dark else 'false'};

        function rnd(a,b) {{ return a + Math.random()*(b-a); }}

        function make() {{
            return {{
                x:  rnd(0, c.width),
                y:  rnd(c.height, c.height * 1.4),
                r:  rnd(3, 14),
                vy: rnd(0.15, 0.55),
                vx: rnd(-0.12, 0.12),
                o:  rnd(isDark ? 0.04 : 0.03, isDark ? 0.14 : 0.09),
                h:  rnd(180, 200),
            }};
        }}

        for (let i=0; i<N; i++) {{
            const b = make();
            b.y = rnd(0, c.height);
            bs.push(b);
        }}

        function frame() {{
            ctx.clearRect(0, 0, c.width, c.height);
            bs.forEach(b => {{
                b.y -= b.vy;
                b.x += b.vx;
                if (b.y + b.r < 0) Object.assign(b, make());

                const g = ctx.createRadialGradient(
                    b.x - b.r * 0.28, b.y - b.r * 0.28, b.r * 0.05,
                    b.x, b.y, b.r
                );
                g.addColorStop(0, `hsla(${{b.h}},90%,80%,${{b.o * 1.4}})`);
                g.addColorStop(0.6, `hsla(${{b.h}},75%,55%,${{b.o}})`);
                g.addColorStop(1, `hsla(${{b.h}},70%,40%,${{b.o * 0.6}})`);

                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fillStyle = g;
                ctx.fill();

                /* inner highlight */
                ctx.beginPath();
                ctx.arc(b.x - b.r*0.25, b.y - b.r*0.25, b.r*0.22, 0, Math.PI*2);
                ctx.fillStyle = `hsla(${{b.h}},100%,95%,${{b.o * 1.2}})`;
                ctx.fill();
            }});
            requestAnimationFrame(frame);
        }}
        frame();
    }}
    boot();
}})();
</script>
""", unsafe_allow_html=True)