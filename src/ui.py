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
        --content-width: 42rem;
    }

    * { font-family: 'Inter', system-ui, sans-serif; }

    .stApp {
        background-color: var(--bg);
    }

    .block-container {
        max-width: 56rem !important;
        padding-top: 1rem !important;
    }

    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
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

    .search-section {
        max-width: var(--content-width);
        margin: 0 auto;
        padding: 0 1rem;
    }

    .stChatInput {
        max-width: var(--content-width);
        margin: 0 auto;
    }

    .stChatInput textarea {
        background-color: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        color: var(--fg) !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 15px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .stChatInput textarea::placeholder {
        color: var(--faint) !important;
    }

    .stChatInput textarea:focus {
        border-color: var(--border-strong) !important;
        box-shadow: 0 0 0 1px var(--border-strong) !important;
    }

    div[data-testid="stChatInput"] {
        position: relative;
    }

    .answer-section {
        max-width: var(--content-width);
        margin: 0 auto;
        padding: 0 1rem;
    }

    .answer-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
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

    .section-label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--faint);
        font-family: 'Inter', ui-monospace, monospace;
        margin-bottom: 0.75rem;
        max-width: var(--content-width);
        margin-left: auto;
        margin-right: auto;
        padding: 0 1rem;
    }

    .source-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.15s ease;
        max-width: var(--content-width);
        margin-left: auto;
        margin-right: auto;
    }

    .source-card:hover {
        border-color: var(--border-strong);
    }

    .source-card .label {
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--faint);
        font-family: 'Inter', ui-monospace, monospace;
        margin-bottom: 0.2rem;
    }

    .source-card .label .source-file {
        color: var(--muted);
    }

    .source-card .source-preview {
        font-size: 13px;
        color: var(--muted);
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .user-message {
        max-width: var(--content-width);
        margin: 0 auto 1rem;
        padding: 0 1rem;
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
        max-width: 80%;
    }

    .sidebar-brand {
        padding: 0.5rem 0 1rem;
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
        min-width: 260px !important;
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

    @media (max-width: 640px) {
        .hero { padding: 1.5rem 0.5rem 1rem; }
        .hero h1 { font-size: 1.6rem; }
        .answer-card { padding: 1rem; border-radius: var(--radius); }
        .user-message .bubble { max-width: 95%; font-size: 13px; }
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
    <div style="text-align:center; padding: 2rem 1rem 3rem; animation: fadeIn 0.3s ease;">
        <div style="font-size:13px; color:var(--faint); font-family:'Inter',ui-monospace,monospace; letter-spacing:0.05em;">
            {EMPTY_UPLOAD_TEXT}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_answer(answer: str, sources: list, chunks: list):
    st.markdown(f"""
    <div class="answer-card fade-in">
        <div class="content">{answer}</div>
    </div>
    """, unsafe_allow_html=True)

    if sources:
        st.markdown('<div class="section-label">Sources</div>', unsafe_allow_html=True)
        for chunk in chunks:
            source_name = Path(chunk["source"]).name if chunk["source"] else "Unknown"
            page_info = f" · p.{chunk['page']}" if chunk.get("page") is not None else ""
            preview = chunk.get("content", "")
            st.markdown(f"""
            <div class="source-card fade-in">
                <div class="label"><span class="source-file">{source_name}</span>{page_info}</div>
                <div class="source-preview">{preview}...</div>
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
