import streamlit as st
import tempfile
import os
import time

st.set_page_config(
    page_title="Nexus AI",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg:        #0a0c0f;
    --surface:   #111318;
    --border:    #1e2128;
    --border2:   #2a2f3a;
    --accent:    #00e5a0;
    --accent2:   #00b8d4;
    --warn:      #ff6b35;
    --text:      #e8eaf0;
    --muted:     #5a6070;
    --card:      #13161c;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,229,160,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(0,184,212,0.05) 0%, transparent 60%),
        var(--bg) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], footer { display: none !important; }

[data-testid="stSidebar"] { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* Main layout */
.block-container {
    max-width: 1100px !important;
    padding: 0 2rem 4rem !important;
    margin: 0 auto !important;
}

/* Hero header */
.hero {
    padding: 3.5rem 0 2.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
    position: relative;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 120px; height: 1px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-tag::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
    margin-bottom: 0.75rem;
}
.hero-title span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--muted);
    font-weight: 300;
}

/* Agent pipeline strip */
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 2.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}
.pipe-step {
    flex: 1;
    padding: 1rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    border-right: 1px solid var(--border);
    position: relative;
}
.pipe-step:last-child { border-right: none; }
.pipe-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.pipe-icon.quality { background: rgba(0,229,160,0.12); }
.pipe-icon.security { background: rgba(255,107,53,0.12); }
.pipe-icon.decision { background: rgba(0,184,212,0.12); }
.pipe-label { font-size: 0.78rem; font-weight: 600; color: var(--text); }
.pipe-desc { font-size: 0.68rem; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
.pipe-arrow {
    color: var(--border2);
    font-size: 0.7rem;
    padding: 0 0.5rem;
}

/* Upload zone */
.upload-label {
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

[data-testid="stFileUploader"] {
    background: var(--card) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] > div {
    background: transparent !important;
    padding: 2rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* File info card */
.file-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 1rem;
}
.file-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--text);
    font-weight: 500;
}
.file-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.2rem;
}
.file-badge {
    background: rgba(0,229,160,0.1);
    color: var(--accent);
    border: 1px solid rgba(0,229,160,0.2);
    border-radius: 6px;
    padding: 0.25rem 0.6rem;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
}

/* Run button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #0a0c0f !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 1.25rem !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(0,229,160,0.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Spinner override */
[data-testid="stSpinner"] {
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}
[data-testid="stSpinner"] > div { color: var(--accent) !important; }

/* Status bar during run */
.status-bar {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin: 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.status-dot {
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 1.2s infinite;
    flex-shrink: 0;
}
.status-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--muted);
}
.status-text strong { color: var(--accent); }

/* Results section */
.results-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.results-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.results-badge {
    background: rgba(0,229,160,0.1);
    color: var(--accent);
    border: 1px solid rgba(0,229,160,0.2);
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.08em;
}

.result-block {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c8cdd8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 600px;
    overflow-y: auto;
}

/* Success / error alerts */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 2rem 0 !important;
}

/* Stat chips row */
.chips {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.chip span { color: var(--text); font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">Code Review Engine . </> </div>
    <div class="hero-title">Nexus<span> AI</span>⚡</span></div>
    <div class="hero-sub">// Automated code review system powered by three specialist agents</div>
</div>
""", unsafe_allow_html=True)

# ── Agent Pipeline Strip ───────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline">
    <div class="pipe-step">
        <div class="pipe-icon quality">֎</div>
        <div>
            <div class="pipe-label">Code Quality Agent</div>
            <div class="pipe-desc">smells · patterns · efficiency</div>
        </div>
    </div>
    <div class="pipe-step">
        <div class="pipe-icon security">⛊</div>
        <div>
            <div class="pipe-label">Security Agent</div>
            <div class="pipe-desc">vulns · injection · leaks</div>
        </div>
    </div>
    <div class="pipe-step">
        <div class="pipe-icon decision">🦈</div>
        <div>
            <div class="pipe-label">Decision Agent</div>
            <div class="pipe-desc">approve · reject · reason</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stat chips ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chips">
    <div class="chip">Model <span>gemini-2.5-flash</span></div>
    <div class="chip">Agents <span>3 specialist</span></div>
    <div class="chip">Framework <span>CrewAI</span></div>
</div>
""", unsafe_allow_html=True)

# ── Upload ────────────────────────────────────────────────────────────────────
st.markdown('<div class="upload-label">// Upload source file</div>', unsafe_allow_html=True)

file = st.file_uploader(
    label="upload",
    label_visibility="collapsed",
    type=["py", "js", "ts", "java", "go", "cpp", "c", "rb", "php", "txt"]
)

if file:
    size_kb = round(len(file.getvalue()) / 1024, 1)
    ext = file.name.split(".")[-1].upper()
    st.markdown(f"""
    <div class="file-card">
        <div>
            <div class="file-name">📄 {file.name}</div>
            <div class="file-meta">{size_kb} KB · {ext} file · ready for review</div>
        </div>
        <div class="file-badge">LOADED</div>
    </div>
    """, unsafe_allow_html=True)

    run = st.button("⬡  Run Agent Review", use_container_width=True)

    if run:
        from crew import run_review

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
            tmp.write(file.read())
            path = tmp.name

        st.markdown("""
        <div class="status-bar">
            <div class="status-dot"></div>
            <div class="status-text">
                <strong>Agents running</strong> · Analyzing code quality → Security review → Making decision...
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Processing through agent pipeline..."):
            try:
                result = run_review(path)
                os.unlink(path)

                st.markdown("---")
                st.markdown("""
                <div class="results-header">
                    <div class="results-title">Review Complete</div>
                    <div class="results-badge">✓ ALL AGENTS DONE</div>
                </div>
                """, unsafe_allow_html=True)

                result_text = str(result)
                st.markdown(f'<div class="result-block">{result_text}</div>', unsafe_allow_html=True)

            except Exception as e:
                os.unlink(path)
                st.error(f"Agent pipeline error: {str(e)}")

else:
    st.markdown("""
    <div style="
        text-align: center;
        padding: 3rem 0 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #2a2f3a;
        letter-spacing: 0.08em;
    ">
        ↑ drop a file to begin
    </div>
    """, unsafe_allow_html=True)