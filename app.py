import streamlit as st
from pathlib import Path
import os
import base64

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gotham File Vault",
    page_icon="🦇",
    layout="centered",
)

# ── Batman CSS ────────────────────────────────────────────────────────────────
BATMAN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ── Root palette ── */
:root {
    --bat-black:   #0a0a0f;
    --bat-dark:    #111118;
    --bat-panel:   #16161f;
    --bat-card:    #1c1c28;
    --bat-border:  #2a2a3a;
    --bat-yellow:  #f5c518;
    --bat-gold:    #d4a017;
    --bat-amber:   #ffb703;
    --bat-gray:    #8888aa;
    --bat-red:     #c0392b;
    --bat-green:   #1e8c45;
    --bat-white:   #e8e8f0;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: var(--bat-black) !important;
    color: var(--bat-white) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bat-dark); }
::-webkit-scrollbar-thumb { background: var(--bat-yellow); border-radius: 3px; }

/* ── Main container ── */
.main .block-container {
    padding: 2rem 2rem 4rem;
    max-width: 800px;
    background: var(--bat-black);
}

/* ── Header / Hero ── */
.bat-hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    background: linear-gradient(180deg, #0a0a0f 0%, #111118 100%);
    border-bottom: 2px solid var(--bat-yellow);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.bat-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 3px;
    background: var(--bat-yellow);
    box-shadow: 0 0 20px var(--bat-yellow), 0 0 40px var(--bat-amber);
}
.bat-logo {
    font-size: 5rem;
    line-height: 1;
    filter: drop-shadow(0 0 12px rgba(245,197,24,0.5));
    animation: batpulse 3s ease-in-out infinite;
}
@keyframes batpulse {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(245,197,24,0.4)); }
    50%       { filter: drop-shadow(0 0 24px rgba(245,197,24,0.9)); }
}
.bat-title {
    font-family: 'Cinzel', serif;
    font-size: 2.6rem;
    font-weight: 900;
    color: var(--bat-yellow);
    text-shadow: 0 0 20px rgba(245,197,24,0.6), 2px 2px 0 #000;
    letter-spacing: 4px;
    margin: 0.3rem 0 0.2rem;
    text-transform: uppercase;
}
.bat-subtitle {
    font-size: 1rem;
    color: var(--bat-gray);
    letter-spacing: 6px;
    text-transform: uppercase;
    font-weight: 300;
}

/* ── Section card ── */
.bat-card {
    background: var(--bat-card);
    border: 1px solid var(--bat-border);
    border-top: 3px solid var(--bat-yellow);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.5), inset 0 1px 0 rgba(245,197,24,0.05);
}

/* ── Section heading ── */
.bat-section-title {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--bat-yellow);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--bat-border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Alert boxes ── */
.bat-alert {
    padding: 0.9rem 1.2rem;
    border-radius: 3px;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 1rem;
    border-left: 4px solid;
}
.bat-alert-success {
    background: rgba(30, 140, 69, 0.15);
    border-color: var(--bat-green);
    color: #4ade80;
}
.bat-alert-error {
    background: rgba(192, 57, 43, 0.15);
    border-color: var(--bat-red);
    color: #f87171;
}
.bat-alert-info {
    background: rgba(245, 197, 24, 0.08);
    border-color: var(--bat-yellow);
    color: var(--bat-yellow);
}

/* ── File content display ── */
.bat-file-content {
    background: #0d0d14;
    border: 1px solid var(--bat-border);
    border-left: 3px solid var(--bat-amber);
    border-radius: 3px;
    padding: 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 0.88rem;
    color: #c8c8e8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 280px;
    overflow-y: auto;
    margin-top: 0.8rem;
    line-height: 1.6;
}

/* ── Streamlit widget overrides ── */
/* Tabs */
[data-baseweb="tab-list"] {
    background: var(--bat-dark) !important;
    border-bottom: 2px solid var(--bat-yellow) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--bat-gray) !important;
    padding: 0.8rem 1.4rem !important;
    border-radius: 0 !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.2s !important;
}
[data-baseweb="tab"]:hover { color: var(--bat-yellow) !important; }
[aria-selected="true"][data-baseweb="tab"] {
    color: var(--bat-yellow) !important;
    background: rgba(245,197,24,0.08) !important;
    border-bottom: 3px solid var(--bat-yellow) !important;
}
[data-testid="stTabContent"] { padding: 1.5rem 0 0 !important; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #0d0d14 !important;
    border: 1px solid var(--bat-border) !important;
    border-radius: 3px !important;
    color: var(--bat-white) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 0.9rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--bat-yellow) !important;
    box-shadow: 0 0 0 2px rgba(245,197,24,0.2) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
    color: var(--bat-gray) !important;
    font-size: 0.82rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* Radio */
[data-testid="stRadio"] label { color: var(--bat-white) !important; font-size: 0.95rem !important; }
[data-testid="stRadio"] > div { gap: 0.4rem !important; }

/* Buttons */
[data-testid="stButton"] > button {
    background: var(--bat-yellow) !important;
    color: #0a0a0f !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(245,197,24,0.3) !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--bat-amber) !important;
    box-shadow: 0 4px 20px rgba(245,197,24,0.55) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bat-panel) !important;
    border-right: 1px solid var(--bat-border) !important;
}
[data-testid="stSidebar"] * { color: var(--bat-white) !important; }

/* Divider */
hr { border-color: var(--bat-border) !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""

st.markdown(BATMAN_CSS, unsafe_allow_html=True)

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="bat-hero">
    <div class="bat-logo">🦇</div>
    <div class="bat-title">Gotham File Vault</div>
    <div class="bat-subtitle">Dark Knight's File Operations System</div>
</div>
""", unsafe_allow_html=True)

# ── Helper: render alert ──────────────────────────────────────────────────────
def bat_alert(msg, kind="info"):
    icons = {"success": "✔", "error": "✖", "info": "◈"}
    st.markdown(
        f'<div class="bat-alert bat-alert-{kind}">{icons[kind]}&nbsp; {msg}</div>',
        unsafe_allow_html=True,
    )

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_create, tab_read, tab_update, tab_delete = st.tabs([
    "🦇 Create",
    "🔍 Read",
    "⚙ Update",
    "💀 Delete",
])

# ════════════════════════════════════════════════════
# CREATE
# ════════════════════════════════════════════════════
with tab_create:
    st.markdown('<div class="bat-section-title">🦇 &nbsp;Deploy New File</div>', unsafe_allow_html=True)
    fname = st.text_input("File Name", placeholder="e.g. gotham_report.txt", key="c_name")
    fcontent = st.text_area("File Content", placeholder="Write your intel here...", height=160, key="c_content")

    if st.button("⚡ Create File", key="btn_create"):
        if not fname.strip():
            bat_alert("File name cannot be empty, Detective.", "error")
        else:
            path = Path(fname.strip())
            if path.exists():
                bat_alert(f"'{fname}' already exists in the vault.", "error")
            else:
                try:
                    path.write_text(fcontent)
                    bat_alert(f"File '{fname}' deployed to the Bat-Vault successfully.", "success")
                except Exception as e:
                    bat_alert(f"Alfred reports an error: {e}", "error")

# ════════════════════════════════════════════════════
# READ
# ════════════════════════════════════════════════════
with tab_read:
    st.markdown('<div class="bat-section-title">🔍 &nbsp;Retrieve Intel</div>', unsafe_allow_html=True)
    fname_r = st.text_input("File Name", placeholder="e.g. gotham_report.txt", key="r_name")

    if st.button("🔦 Read File", key="btn_read"):
        if not fname_r.strip():
            bat_alert("Provide a file name, Dark Knight.", "error")
        else:
            path = Path(fname_r.strip())
            if not path.exists():
                bat_alert(f"No such file '{fname_r}' in the vault.", "error")
            else:
                try:
                    content = path.read_text()
                    bat_alert(f"Intel retrieved from '{fname_r}'.", "success")
                    st.markdown(
                        f'<div class="bat-file-content">{content if content else "(empty file)"}</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    bat_alert(f"Alfred reports an error: {e}", "error")

# ════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════
with tab_update:
    st.markdown('<div class="bat-section-title">⚙ &nbsp;Modify Operations</div>', unsafe_allow_html=True)
    fname_u = st.text_input("File Name", placeholder="e.g. gotham_report.txt", key="u_name")

    operation = st.radio(
        "Choose Operation",
        ["Rename File", "Append Content", "Overwrite Content"],
        key="u_op",
    )

    if operation == "Rename File":
        new_name = st.text_input("New File Name", placeholder="e.g. batman_log.txt", key="u_newname")
        if st.button("✏ Rename File", key="btn_rename"):
            if not fname_u.strip() or not new_name.strip():
                bat_alert("Fill in both file names.", "error")
            else:
                path = Path(fname_u.strip())
                new_path = Path(new_name.strip())
                if not path.exists():
                    bat_alert(f"'{fname_u}' not found in the vault.", "error")
                elif new_path.exists():
                    bat_alert(f"'{new_name}' already exists.", "error")
                else:
                    try:
                        path.rename(new_path)
                        bat_alert(f"File renamed to '{new_name}' successfully.", "success")
                    except Exception as e:
                        bat_alert(f"Alfred reports an error: {e}", "error")

    elif operation == "Append Content":
        append_data = st.text_area("Content to Append", placeholder="Additional intel...", height=130, key="u_append")
        if st.button("➕ Append to File", key="btn_append"):
            if not fname_u.strip():
                bat_alert("Provide a file name.", "error")
            else:
                path = Path(fname_u.strip())
                if not path.exists():
                    bat_alert(f"'{fname_u}' not found in the vault.", "error")
                else:
                    try:
                        with open(path, "a") as f:
                            f.write("\n" + append_data)
                        bat_alert(f"Intel appended to '{fname_u}' successfully.", "success")
                    except Exception as e:
                        bat_alert(f"Alfred reports an error: {e}", "error")

    else:  # Overwrite
        overwrite_data = st.text_area("New Content", placeholder="Replace all existing intel...", height=130, key="u_overwrite")
        if st.button("🔄 Overwrite File", key="btn_overwrite"):
            if not fname_u.strip():
                bat_alert("Provide a file name.", "error")
            else:
                path = Path(fname_u.strip())
                if not path.exists():
                    bat_alert(f"'{fname_u}' not found in the vault.", "error")
                else:
                    try:
                        path.write_text(overwrite_data)
                        bat_alert(f"'{fname_u}' overwritten successfully.", "success")
                    except Exception as e:
                        bat_alert(f"Alfred reports an error: {e}", "error")

# ════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════
with tab_delete:
    st.markdown('<div class="bat-section-title">💀 &nbsp;Eliminate Target</div>', unsafe_allow_html=True)
    fname_d = st.text_input("File Name", placeholder="e.g. gotham_report.txt", key="d_name")

    # Confirmation guard
    confirm = st.text_input(
        'Type "DESTROY" to confirm',
        placeholder="DESTROY",
        key="d_confirm",
    )

    if st.button("🗑 Delete File", key="btn_delete"):
        if not fname_d.strip():
            bat_alert("Provide a file name, Dark Knight.", "error")
        elif confirm.strip() != "DESTROY":
            bat_alert('You must type "DESTROY" to confirm deletion.', "error")
        else:
            path = Path(fname_d.strip())
            if not path.exists():
                bat_alert(f"'{fname_d}' does not exist in the vault.", "error")
            else:
                try:
                    path.unlink()
                    bat_alert(f"'{fname_d}' has been eliminated from the Bat-Vault.", "success")
                except Exception as e:
                    bat_alert(f"Alfred reports an error: {e}", "error")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    text-align:center;
    margin-top:3rem;
    padding:1.2rem;
    border-top:1px solid #2a2a3a;
    font-size:0.78rem;
    color:#555577;
    letter-spacing:3px;
    text-transform:uppercase;
    font-family:'Rajdhani',sans-serif;
">
    🦇 &nbsp; Gotham File Vault &nbsp;·&nbsp; Protected by the Dark Knight &nbsp; 🦇
</div>
""", unsafe_allow_html=True)