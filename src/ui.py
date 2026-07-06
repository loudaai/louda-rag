import streamlit as st
from pathlib import Path

from src.vector_store import count_documents
from src.prompts import WELCOME_TEXT, EMPTY_UPLOAD_TEXT


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #0c0c0f;
        --fg: #f4f4f5;
        --surface: #18181b;
        --surface-strong: #1e1e22;
        --border: #2a2a30;
        --border-strong: #3a3a42;
        --muted: #a0a0a8;
        --faint: #8a8a92;
        --radius: 12px;
        --radius-lg: 16px;
        --content-w: 760px;
    }

    * { font-family: 'Inter', system-ui, sans-serif; }

    .stApp { background-color: var(--bg); }

    /* --- LAYOUT : single centered column --- */

    .main .block-container {
        max-width: var(--content-w) !important;
        padding: 0 1rem !important;
        margin: 0 auto !important;
    }

    /* --- Streamlit chrome reset --- */

    *:focus, *:focus-visible, *:active {
        outline: none !important;
        box-shadow: none !important;
        border-color: var(--border) !important;
    }

    *::-moz-focus-inner { border: 0 !important; }

    button:focus, button:focus-visible, button:active {
        outline: none !important;
        box-shadow: none !important;
    }

    textarea:focus, textarea:focus-visible, textarea:active,
    input:focus, input:focus-visible, input:active {
        outline: none !important;
        box-shadow: none !important;
    }

    .st-emotion-cache-1gv3huu, .st-emotion-cache-1dp5vir {
        background-color: transparent !important;
    }

    /* --- HERO --- */

    .hero {
        text-align: center;
        padding: 3.5rem 0 1.25rem;
        animation: fadeIn 0.3s ease;
    }

    .hero h1 {
        font-size: 2.25rem;
        font-weight: 600;
        letter-spacing: -0.03em;
        color: var(--fg);
        margin: 0;
        line-height: 1.15;
    }

    .hero .micro {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--faint);
        font-family: 'Inter', ui-monospace, monospace;
        margin-top: 0.5rem;
    }

    .hero .sub {
        font-size: 14px;
        color: var(--muted);
        margin-top: 0.4rem;
        font-weight: 400;
    }

    /* --- CHAT INPUT --- */

    .stChatInput {
        max-width: var(--content-w) !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .stChatInput textarea {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        color: var(--fg) !important;
        padding: 0.85rem 3.2rem 0.85rem 1.5rem !important;
        font-size: 15px !important;
        caret-color: var(--fg) !important;
        min-height: 52px !important;
        transition: border-color 0.15s ease;
        resize: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stChatInput textarea::placeholder {
        color: var(--faint) !important;
        opacity: 0.6;
    }

    .stChatInput textarea:focus {
        border-color: var(--border-strong) !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* send button wrapper reset */
    div[data-testid="stChatInput"] {
        position: relative !important;
    }

    div[data-testid="stChatInput"] > div:first-child {
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stChatInput"] button {
        position: absolute !important;
        right: 7px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 38px !important;
        height: 38px !important;
        border-radius: 50% !important;
        background: var(--fg) !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        padding: 0 !important;
        z-index: 1 !important;
        outline: none !important;
        box-shadow: none !important;
        transition: opacity 0.15s ease, transform 0.15s ease;
    }

    div[data-testid="stChatInput"] button:hover {
        opacity: 0.8;
        transform: translateY(-50%) scale(1.04) !important;
        background: var(--fg) !important;
    }

    div[data-testid="stChatInput"] button:focus,
    div[data-testid="stChatInput"] button:focus-visible,
    div[data-testid="stChatInput"] button:active {
        outline: none !important;
        box-shadow: none !important;
        background: var(--fg) !important;
    }

    div[data-testid="stChatInput"] button svg {
        fill: var(--bg) !important;
        width: 16px !important;
        height: 16px !important;
    }

    div[data-testid="stChatInput"] button:disabled {
        background: var(--surface-strong) !important;
        opacity: 0.35;
    }

    div[data-testid="stChatInput"] button:disabled svg {
        fill: var(--faint) !important;
    }

    /* --- ANSWER CARD --- */

    .answer-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin: 0 0 1.25rem;
    }

    .answer-card .content {
        font-size: 15px;
        color: var(--fg);
        line-height: 1.7;
    }

    .answer-card .content p:last-child { margin-bottom: 0; }

    /* --- USER MESSAGE --- */

    .user-message {
        text-align: right;
        margin: 0 0 1rem;
    }

    .user-message .bubble {
        display: inline-block;
        background: var(--surface-strong);
        border: 1px solid var(--border);
        border-radius: 18px 18px 4px 18px;
        padding: 0.6rem 1.2rem;
        font-size: 14px;
        color: var(--fg);
        line-height: 1.5;
        max-width: 72%;
    }

    /* --- SIDEBAR --- */

    section[data-testid="stSidebar"] {
        background-color: var(--bg);
        border-right: 1px solid var(--border);
        min-width: 230px !important;
        max-width: 260px !important;
    }

    section[data-testid="stSidebar"] .st-emotion-cache-1gv3huu {
        background-color: var(--bg);
    }

    .sidebar-brand { padding: 0 0 1rem; }

    .sidebar-brand .logo {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: var(--fg);
    }

    .sidebar-brand .tagline {
        font-size: 11px;
        color: var(--faint);
        margin-top: 0.1rem;
    }

    .sidebar-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--faint);
        font-family: 'Inter', ui-monospace, monospace;
        margin-bottom: 0.5rem;
    }

    .status-line {
        font-size: 13px;
        color: var(--muted);
        line-height: 1.6;
    }

    .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        margin-right: 6px;
        vertical-align: middle;
    }

    .status-dot.active { background-color: #22c55e; }

    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        opacity: 0.5;
        margin: 1rem 0;
    }

    /* --- FILE UPLOADER --- */

    div[data-testid="stFileUploader"] section {
        border: 1px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        background: transparent !important;
        padding: 1.2rem !important;
        transition: border-color 0.15s ease;
    }

    div[data-testid="stFileUploader"] section:hover {
        border-color: var(--border-strong) !important;
    }

    div[data-testid="stFileUploader"] button {
        background: var(--surface-strong) !important;
        color: var(--muted) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        padding: 0.3rem 1rem !important;
    }

    /* --- BUTTONS : all minimal --- */

    .stButton button {
        background: transparent !important;
        color: var(--muted) !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 0.35rem 0.85rem !important;
        transition: background 0.15s ease, color 0.15s ease !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stButton button:hover {
        background: var(--surface) !important;
        color: var(--fg) !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stButton button:focus, .stButton button:focus-visible, .stButton button:active {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
        background: var(--surface) !important;
    }

    /* sidebar "clear" button - even more minimal */
    section[data-testid="stSidebar"] .stButton button {
        font-size: 11px !important;
        padding: 0.25rem 0 !important;
        color: var(--faint) !important;
        border: none !important;
        width: auto !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        color: var(--muted) !important;
        background: transparent !important;
    }

    /* --- SPINNER --- */

    .stSpinner > div {
        border-color: var(--border-strong) !important;
        border-top-color: var(--fg) !important;
        width: 20px !important;
        height: 20px !important;
    }

    /* --- INGESTION TOAST --- */

    .ingest-toast {
        text-align: center;
        font-size: 12px;
        color: var(--muted);
        padding: 0.15rem 0;
    }

    .ingest-toast.error { color: #ef4444; }

    /* --- HIDE STREAMLIT CHROME --- */

    footer { display: none !important; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }

    /* --- ANIMATIONS --- */

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in { animation: fadeIn 0.3s ease; }

    /* --- RESPONSIVE --- */

    @media (max-width: 820px) {
        :root { --content-w: 100%; }

        .main .block-container {
            padding: 0 0.75rem !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
            border-right: none !important;
            border-bottom: 1px solid var(--border);
        }

        .hero { padding: 2rem 0 1rem; }
        .hero h1 { font-size: 1.5rem; }

        .answer-card { padding: 1rem; }

        .user-message .bubble { max-width: 100%; }

        .stChatInput textarea {
            font-size: 14px !important;
            padding: 0.75rem 2.8rem 0.75rem 1rem !important;
            min-height: 46px !important;
        }

        div[data-testid="stChatInput"] button {
            width: 34px !important;
            height: 34px !important;
            right: 5px !important;
        }
    }

    @media (max-width: 480px) {
        .hero h1 { font-size: 1.25rem; }
        .hero .sub { font-size: 13px; }
        .hero { padding: 1.5rem 0 0.75rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_welcome():
    st.markdown(f"""
    <div class="hero fade-in">
        <h1>LOUDA AI</h1>
        <div class="micro">ask the knowledge base</div>
        <div class="sub">{WELCOME_TEXT}</div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown(f"""
    <div style="text-align:center; padding: 1.5rem 0 2.5rem; animation: fadeIn 0.3s ease;">
        <div style="font-size:13px; color:var(--faint); font-family:'Inter',ui-monospace,monospace; letter-spacing:0.05em;">
            {EMPTY_UPLOAD_TEXT}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_answer(answer: str):
    st.markdown(f"""
    <div class="answer-card fade-in">
        <div class="content">{answer}</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="logo">Louda AI</div>
            <div class="tagline">Personal Knowledge RAG</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        doc_count = count_documents()
        st.markdown(f"""
        <div class="status-line">
            <span class="status-dot active"></span>System Online
        </div>
        <div class="status-line" style="margin-top:0.25rem;">
            Documents: {doc_count}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Upload</div>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if doc_count > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Clear knowledge base", use_container_width=True):
                from src.vector_store import delete_all
                delete_all()
                st.rerun()

        return uploaded_files


def render_ingestion_status(success: bool, name: str):
    if success:
        st.markdown(f"""
        <div class="ingest-toast">✓ {name} ingested</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ingest-toast error">✗ Failed to ingest {name}</div>
        """, unsafe_allow_html=True)
