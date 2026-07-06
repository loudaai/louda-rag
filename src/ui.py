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
        --content-width: 46rem;
    }

    * { font-family: 'Inter', system-ui, sans-serif; }

    .stApp {
        background-color: var(--bg);
    }

    .main > .block-container {
        max-width: var(--content-width) !important;
        padding: 1.5rem 1rem 5rem !important;
        margin: 0 auto !important;
    }

    section[data-testid="stSidebar"] + .main .block-container {
        max-width: var(--content-width) !important;
        padding: 1.5rem 1rem 5rem !important;
        margin: 0 auto !important;
    }

    .hero {
        text-align: center;
        padding: 2.5rem 0 1.5rem;
        animation: fadeIn 0.3s ease;
    }

    .hero h1 {
        font-size: 2.2rem;
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

    .stChatInput {
        max-width: var(--content-width) !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    .stChatInputContainer {
        border: none !important;
    }

    .stChatInput textarea {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        color: var(--fg) !important;
        padding: 0.75rem 3rem 0.75rem 1.25rem !important;
        font-size: 15px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        min-height: 48px !important;
    }

    .stChatInput textarea::placeholder {
        color: var(--faint) !important;
    }

    .stChatInput textarea:focus {
        border-color: var(--border-strong) !important;
        box-shadow: 0 0 0 1px var(--border-strong) !important;
    }

    div[data-testid="stChatInput"] button {
        position: absolute !important;
        right: 6px !important;
        top: 6px !important;
        width: 36px !important;
        height: 36px !important;
        border-radius: 50% !important;
        background: var(--fg) !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        padding: 0 !important;
        z-index: 1 !important;
    }

    div[data-testid="stChatInput"] button:hover {
        opacity: 0.85;
    }

    div[data-testid="stChatInput"] button svg {
        fill: var(--bg) !important;
        width: 16px !important;
        height: 16px !important;
    }

    div[data-testid="stChatInput"] button:disabled {
        background: var(--surface-strong) !important;
        opacity: 0.4;
    }

    div[data-testid="stChatInput"] button:disabled svg {
        fill: var(--faint) !important;
    }

    .answer-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        max-width: var(--content-width);
        margin-left: auto;
        margin-right: auto;
    }

    .answer-card .content {
        font-size: 15px;
        color: var(--fg);
        line-height: 1.7;
    }

    .answer-card .content p {
        margin: 0 0 0.75rem;
    }

    .answer-card .content p:last-child {
        margin-bottom: 0;
    }

    .user-message {
        max-width: var(--content-width);
        margin: 0 auto 1rem;
        text-align: right;
    }

    .user-message .bubble {
        display: inline-block;
        background: var(--surface-strong);
        border: 1px solid var(--border);
        border-radius: 18px 18px 4px 18px;
        padding: 0.6rem 1.1rem;
        font-size: 14px;
        color: var(--fg);
        line-height: 1.5;
        max-width: 75%;
    }

    .sidebar-brand {
        padding: 0.25rem 0 1rem;
    }

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

    .sidebar-section {
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

    div[data-testid="stFileUploader"] section {
        border: 1px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        background: transparent !important;
        padding: 1.2rem !important;
    }

    div[data-testid="stFileUploader"] section:hover {
        border-color: var(--border-strong) !important;
    }

    .stButton button {
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 0.35rem 1rem !important;
        background: var(--fg) !important;
        color: var(--bg) !important;
        border: none !important;
        transition: opacity 0.15s ease;
    }

    .stButton button:hover {
        opacity: 0.85;
        background: var(--fg) !important;
    }

    .stButton button[kind="secondary"] {
        background: transparent !important;
        color: var(--muted) !important;
        border: 1px solid var(--border) !important;
    }

    .stButton button[kind="secondary"]:hover {
        border-color: var(--border-strong) !important;
        color: var(--fg) !important;
    }

    .stSpinner > div {
        border-color: var(--border-strong) !important;
        border-top-color: var(--fg) !important;
        width: 20px !important;
        height: 20px !important;
    }

    .ingest-toast {
        text-align: center;
        font-size: 13px;
        color: var(--muted);
        padding: 0.25rem 0;
    }

    .ingest-toast.error {
        color: #ef4444;
    }

    hr {
        border-color: var(--border) !important;
        opacity: 0.5;
        margin: 1rem 0;
    }

    footer { display: none !important; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background-color: var(--bg);
        border-right: 1px solid var(--border);
        min-width: 240px !important;
        max-width: 280px !important;
        width: 260px !important;
    }

    section[data-testid="stSidebar"] .st-emotion-cache-1gv3huu {
        background-color: var(--bg);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.3s ease;
    }

    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
            width: 100% !important;
            border-right: none !important;
            border-bottom: 1px solid var(--border);
            position: relative !important;
        }

        .main > .block-container,
        section[data-testid="stSidebar"] + .main .block-container {
            max-width: 100% !important;
            padding: 1rem 0.75rem 6rem !important;
        }

        .hero { padding: 1.5rem 0 1rem; }
        .hero h1 { font-size: 1.5rem; }

        .answer-card {
            padding: 1rem;
            border-radius: var(--radius);
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        .user-message .bubble {
            max-width: 100%;
            font-size: 13px;
        }

        .stChatInput textarea {
            font-size: 14px !important;
            padding: 0.65rem 2.8rem 0.65rem 1rem !important;
        }

        div[data-testid="stChatInput"] button {
            right: 4px !important;
            top: 4px !important;
            width: 32px !important;
            height: 32px !important;
        }
    }

    @media (max-width: 480px) {
        .hero h1 { font-size: 1.3rem; }
        .hero .sub { font-size: 13px; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(doc_count: int):
    if doc_count > 0:
        st.markdown("""
        <div class="hero">
            <h1>LOUDA AI</h1>
            <div class="micro">ask the knowledge base</div>
        </div>
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
    <div style="text-align:center; padding: 2rem 0 3rem; animation: fadeIn 0.3s ease;">
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
        st.markdown('<div class="sidebar-section">Upload</div>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if doc_count > 0:
            if st.button("Clear Knowledge Base", use_container_width=True, type="secondary"):
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
