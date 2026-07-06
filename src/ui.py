import streamlit as st
from pathlib import Path

from src.config import CHROMA_DIR
from src.vector_store import count_documents
from src.prompts import WELCOME_TEXT, EMPTY_UPLOAD_TEXT


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', system-ui, sans-serif; }

    .stApp {
        background-color: #0c0c0f;
    }

    .main-header {
        text-align: center;
        padding: 3rem 1rem 1.5rem;
    }

    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: #f4f4f5;
        margin: 0;
        line-height: 1.2;
    }

    .main-header .micro-label {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #8a8a92;
        margin-top: 0.5rem;
        font-family: 'Geist Mono', ui-monospace, monospace;
    }

    .main-header .subtitle {
        font-size: 15px;
        color: #a0a0a8;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    .search-container {
        max-width: 42rem;
        margin: 0 auto;
        padding: 0 1rem;
    }

    .source-card {
        background: #18181b;
        border: 1px solid #2a2a30;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.15s ease;
    }

    .source-card:hover {
        border-color: #3a3a42;
    }

    .source-card .label {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #8a8a92;
        font-family: 'Geist Mono', ui-monospace, monospace;
        margin-bottom: 0.25rem;
    }

    .source-card .content {
        font-size: 13px;
        color: #a0a0a8;
        line-height: 1.5;
    }

    .answer-card {
        background: #18181b;
        border: 1px solid #2a2a30;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        max-width: 42rem;
        margin-left: auto;
        margin-right: auto;
    }

    .answer-card .content {
        font-size: 15px;
        color: #f4f4f5;
        line-height: 1.7;
    }

    .section-label {
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #8a8a92;
        font-family: 'Geist Mono', ui-monospace, monospace;
        margin-bottom: 0.75rem;
        max-width: 42rem;
        margin-left: auto;
        margin-right: auto;
        padding: 0 1rem;
    }

    .sidebar-info {
        font-size: 13px;
        color: #a0a0a8;
        line-height: 1.5;
    }

    .stChatInput textarea {
        background-color: #18181b !important;
        border: 1px solid #2a2a30 !important;
        border-radius: 24px !important;
        color: #f4f4f5 !important;
        padding: 0.75rem 1.25rem !important;
        font-size: 15px !important;
    }

    .stChatInput textarea:focus {
        border-color: #3a3a42 !important;
        box-shadow: none !important;
    }

    div[data-testid="stFileUploader"] {
        max-width: 42rem;
        margin: 0 auto;
    }

    div[data-testid="stFileUploader"] section {
        border: 1px dashed #2a2a30 !important;
        border-radius: 12px !important;
        background: transparent !important;
        padding: 1.5rem !important;
    }

    .stButton button {
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        background: #f4f4f5 !important;
        color: #0c0c0f !important;
        border: none !important;
    }

    .stButton button:hover {
        background: #e4e4e7 !important;
    }

    .divider {
        max-width: 42rem;
        margin: 2rem auto;
        border: none;
        border-top: 1px solid #2a2a30;
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
    .status-dot.inactive { background-color: #8a8a92; }

    footer { display: none !important; }
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="main-header">
            <h1>LOUDA AI</h1>
            <div class="micro-label">Ask the Knowledge Base</div>
        </div>
        """, unsafe_allow_html=True)


def render_answer(answer: str, sources: list, chunks: list):
    st.markdown(f"""
    <div class="answer-card">
        <div class="content">{answer}</div>
    </div>
    """, unsafe_allow_html=True)

    if sources:
        st.markdown('<div class="section-label">Sources</div>', unsafe_allow_html=True)
        for chunk in chunks:
            source_name = Path(chunk["source"]).name if chunk["source"] else "Unknown"
            page_info = f" · page {chunk['page']}" if chunk.get("page") is not None else ""
            st.markdown(f"""
            <div class="source-card">
                <div class="label">{source_name}{page_info}</div>
                <div class="content">{chunk['content']}...</div>
            </div>
            """, unsafe_allow_html=True)


def render_welcome():
    st.markdown(f"""
    <div style="text-align:center; padding: 2rem 1rem;">
        <div style="font-size:15px; color:#a0a0a8; max-width:32rem; margin:0 auto; line-height:1.6;">
            {WELCOME_TEXT}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown(f"""
    <div style="text-align:center; padding: 3rem 1rem;">
        <div style="font-size:13px; color:#8a8a92; font-family:'Geist Mono',ui-monospace,monospace; letter-spacing:0.05em;">
            {EMPTY_UPLOAD_TEXT}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <div style="font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:#8a8a92; font-family:'Geist Mono',ui-monospace,monospace;">
                LOUDA AI
            </div>
            <div style="font-size:13px; color:#a0a0a8; margin-top:0.25rem;">
                Personal Knowledge RAG
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        doc_count = count_documents()
        st.markdown(f"""
        <div class="sidebar-info">
            <span class="status-dot active"></span>System Online<br>
            Documents: {doc_count}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div style="font-size:11px; font-weight:500; letter-spacing:0.15em; text-transform:uppercase; color:#8a8a92; font-family:\'Geist Mono\',ui-monospace,monospace; margin-bottom:0.5rem;">Upload</div>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if st.button("Clear Knowledge Base", use_container_width=True):
            from src.vector_store import delete_all
            delete_all()
            st.rerun()

        return uploaded_files


def render_ingestion_status(success: bool, name: str):
    if success:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; font-size:13px; color:#a0a0a8;">
            ✓ {name} ingested
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:0.5rem; font-size:13px; color:#ef4444;">
            ✗ Failed to ingest {name}
        </div>
        """, unsafe_allow_html=True)
