import html
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from src.config import validate_config
from src.document_loader import load_document, chunk_documents
from src.vector_store import add_documents, count_documents
from src.rag import ask
from src.prompts import WELCOME_TEXT, EMPTY_UPLOAD_TEXT


def _safe(value: str) -> str:
    return html.escape(str(value or ""))


def _format_text(value: str) -> str:
    escaped = _safe(value)
    return escaped.replace("\n", "<br>")





def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg: #0c0c0f;
            --bg-soft: #101014;
            --ink: #f4f4f5;
            --muted: #a0a0a8;
            --faint: #8a8a92;
            --surface: #18181b;
            --surface-2: #1e1e22;
            --line: #2a2a30;
            --line-strong: #3a3a42;
            --inverse: #f4f4f5;
            --inverse-text: #0c0c0f;
            --danger: #ef4444;
        }

        * {
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        html, body, [class*="css"] {
            background: var(--bg) !important;
            color: var(--ink) !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top center, rgba(255,255,255,0.055), transparent 34rem),
                linear-gradient(180deg, #0c0c0f 0%, #09090b 100%);
            color: var(--ink);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.22;
            background-image: radial-gradient(circle, rgba(244,244,245,0.55) 1px, transparent 1px);
            background-size: 9px 9px;
            mask-image: radial-gradient(circle at 50% 0%, black 0%, transparent 48%);
            -webkit-mask-image: radial-gradient(circle at 50% 0%, black 0%, transparent 48%);
            z-index: 0;
        }

        .block-container {
            position: relative;
            z-index: 1;
            max-width: 820px !important;
            padding: 2.25rem 1rem 7rem !important;
            margin: 0 auto !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }

        MainMenu, footer {
            visibility: hidden !important;
        }

        /* ---------- sidebar ---------- */

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(24,24,27,0.94), rgba(12,12,15,0.96)) !important;
            border-right: 1px solid var(--line) !important;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.35rem;
        }

        .sidebar-brand {
            padding: 0.25rem 0 0.85rem;
        }

        .sidebar-kicker,
        .micro-label {
            font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 10px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--faint);
        }

        .sidebar-logo {
            margin-top: 0.35rem;
            font-size: 1.08rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            color: var(--ink);
        }

        .sidebar-tagline {
            margin-top: 0.15rem;
            font-size: 12px;
            color: var(--muted);
            line-height: 1.5;
        }

        .side-card {
            border: 1px solid var(--line);
            background: rgba(24,24,27,0.55);
            border-radius: 16px;
            padding: 0.9rem;
            margin: 0.75rem 0;
        }

        .status-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.5;
        }

        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--ink);
            margin-right: 0.4rem;
            animation: pulse 1.8s ease-in-out infinite;
        }

        .doc-number {
            font-family: "JetBrains Mono", monospace;
            color: var(--ink);
            font-size: 12px;
        }

        hr {
            border: none !important;
            border-top: 1px solid var(--line) !important;
            margin: 1rem 0 !important;
        }

        /* ---------- hero ---------- */

        .hero {
            text-align: center;
            padding: 4.75rem 0 2.5rem;
            animation: fadeUp 700ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        .hero-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.28rem 0.65rem;
            border: 1px solid var(--line);
            border-radius: 999px;
            color: var(--muted);
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            background: rgba(24,24,27,0.42);
            margin-bottom: 1rem;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2.4rem, 7vw, 4.6rem);
            line-height: 0.92;
            letter-spacing: -0.08em;
            font-weight: 800;
            color: var(--ink);
        }

        .hero-sub {
            max-width: 34rem;
            margin: 1.05rem auto 0;
            color: var(--muted);
            font-size: 15px;
            line-height: 1.7;
        }

        .hero-stat-row {
            margin: 1.5rem auto 0;
            display: flex;
            justify-content: center;
            gap: 0.6rem;
            flex-wrap: wrap;
        }

        .hero-pill {
            border: 1px solid var(--line);
            border-radius: 999px;
            padding: 0.35rem 0.65rem;
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            color: var(--faint);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            background: rgba(24,24,27,0.38);
        }

        /* ---------- messages ---------- */

        .thread {
            margin-top: 0.75rem;
        }

        .user-message {
            display: flex;
            justify-content: flex-end;
            margin: 0 0 1rem;
            animation: fadeUp 350ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        .user-bubble {
            max-width: min(92%, 620px);
            background: var(--ink);
            color: var(--bg);
            border-radius: 18px 18px 4px 18px;
            padding: 0.72rem 1rem;
            font-size: 14px;
            line-height: 1.55;
            box-shadow: 0 18px 40px -26px rgba(0,0,0,0.75);
        }

        .answer-card {
            position: relative;
            border: 1px solid var(--line);
            border-radius: 20px;
            background:
                linear-gradient(180deg, rgba(30,30,34,0.82), rgba(24,24,27,0.72));
            padding: 1.35rem;
            margin: 0 0 1.2rem;
            box-shadow: 0 22px 50px -36px rgba(0,0,0,0.95);
            animation: fadeUp 420ms cubic-bezier(0.16, 1, 0.3, 1) both;
            overflow: hidden;
        }

        .answer-card::before {
            content: "";
            position: absolute;
            inset: 6px;
            border: 1px solid rgba(244,244,245,0.035);
            border-radius: 15px;
            pointer-events: none;
        }

        .answer-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            margin-bottom: 0.9rem;
        }

        .answer-label {
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            color: var(--faint);
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .answer-badge {
            border: 1px solid var(--line-strong);
            color: var(--muted);
            border-radius: 999px;
            padding: 0.16rem 0.45rem;
            font-family: "JetBrains Mono", monospace;
            font-size: 9px;
            text-transform: uppercase;
            letter-spacing: 0.13em;
        }

        .answer-content {
            color: var(--ink);
            font-size: 15px;
            line-height: 1.78;
        }

        .answer-content strong {
            font-weight: 700;
        }

        .empty-state {
            max-width: 34rem;
            margin: 0 auto 1.75rem;
            border: 1px dashed var(--line);
            border-radius: 18px;
            padding: 1rem;
            color: var(--muted);
            text-align: center;
            font-size: 13px;
            line-height: 1.65;
            background: rgba(24,24,27,0.28);
            animation: fadeUp 760ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        /* ---------- input ---------- */

        div[data-testid="stChatInput"] {
            max-width: 820px !important;
            margin: 0 auto !important;
            position: relative !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stChatInput"] > div {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stChatInput"] textarea {
            background: #18181b !important;
            border: none !important;
            border-radius: 24px !important;
            color: var(--ink) !important;
            min-height: 52px !important;
            padding: 0.85rem 3.2rem 0.85rem 1.25rem !important;
            font-size: 15px !important;
            outline: none !important;
            box-shadow: none !important;
            resize: none !important;
            line-height: 1.5 !important;
        }

        div[data-testid="stChatInput"] textarea:focus {
            outline: none !important;
            box-shadow: none !important;
            border: none !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: var(--faint) !important;
            opacity: 0.6 !important;
        }

        div[data-testid="stChatInput"] button {
            position: absolute !important;
            right: 6px !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            background: #f4f4f5 !important;
            border-radius: 50% !important;
            width: 34px !important;
            height: 34px !important;
            min-width: 34px !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: opacity 180ms ease !important;
            z-index: 1 !important;
            border: none !important;
            box-shadow: none !important;
            cursor: pointer !important;
        }

        div[data-testid="stChatInput"] button:hover {
            opacity: 0.75 !important;
        }

        div[data-testid="stChatInput"] button svg {
            fill: #0c0c0f !important;
            width: 16px !important;
            height: 16px !important;
        }

        /* ---------- upload/buttons ---------- */

        div[data-testid="stFileUploader"] section {
            background: rgba(24,24,27,0.36) !important;
            border: 1px dashed var(--line-strong) !important;
            border-radius: 16px !important;
            padding: 1rem !important;
        }

        div[data-testid="stFileUploader"] section:hover {
            background: rgba(30,30,34,0.55) !important;
            border-color: var(--faint) !important;
        }

        div[data-testid="stFileUploader"] button,
        .stButton button {
            background: transparent !important;
            color: var(--muted) !important;
            border: 1px solid var(--line) !important;
            border-radius: 999px !important;
            font-family: "JetBrains Mono", monospace !important;
            font-size: 10px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            padding: 0.38rem 0.75rem !important;
            transition: all 180ms ease !important;
        }

        div[data-testid="stFileUploader"] button:hover,
        .stButton button:hover {
            color: var(--ink) !important;
            border-color: var(--line-strong) !important;
            background: rgba(244,244,245,0.04) !important;
        }

        .ingest-toast {
            margin: 0.6rem 0;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 0.7rem;
            color: var(--muted);
            font-size: 12px;
            line-height: 1.4;
            background: rgba(24,24,27,0.42);
        }

        .ingest-toast.error {
            color: var(--danger);
        }

        .stAlert {
            border-radius: 16px !important;
        }

        /* ---------- motion ---------- */

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.28; }
        }

        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }

        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 0.8rem 7rem !important;
            }

            .hero {
                padding-top: 2.5rem;
            }

            .hero h1 {
                font-size: 2.7rem;
            }

            .answer-card {
                padding: 1rem;
                border-radius: 16px;
            }

            .user-bubble {
                max-width: 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-kicker">personal rag</div>
                <div class="sidebar-logo">Louda AI</div>
                <div class="sidebar-tagline">A private knowledge assistant built from Louda's documents.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        doc_count = count_documents()

        st.markdown(
            f"""
            <div class="side-card">
                <div class="status-row">
                    <span><span class="status-dot"></span>System online</span>
                    <span class="doc-number">{doc_count}</span>
                </div>
                <div class="status-row" style="margin-top:0.45rem;">
                    <span>Stored chunks</span>
                    <span class="doc-number">{doc_count}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="micro-label">upload knowledge</div>',
                    unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Upload PDFs, TXT, or Markdown files",
            type=["pdf", "txt", "md"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        if doc_count > 0:
            if st.button("Clear knowledge base", use_container_width=True):
                from src.vector_store import delete_all

                delete_all()
                st.session_state.messages = []
                st.session_state.ingested = set()
                st.rerun()

        st.markdown(
            """
            <div style="margin-top:1rem;color:var(--faint);font-size:11px;line-height:1.6;">
                Louda AI only answers from the uploaded knowledge base. If something is missing, it should say Louda has not shared it yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return uploaded_files


def render_welcome(doc_count: int = 0):
    st.markdown(
        f"""
        <section class="hero">
            <h1>Louda AI</h1>
            <div class="hero-sub">{_safe(WELCOME_TEXT)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state():
    st.markdown(
        f"""
        <div class="empty-state">
            {_safe(EMPTY_UPLOAD_TEXT)}
            <br><br>
            Upload Louda's profile, project notes, docs, or markdown files from the sidebar to start.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_user_message(content: str):
    st.markdown(
        f"""
        <div class="user-message">
            <div class="user-bubble">{_format_text(content)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_answer(answer: str):
    st.markdown(
        f"""
        <article class="answer-card">
            <div class="answer-topline">
                <div class="answer-label">Louda AI</div>
            </div>
            <div class="answer-content">{_format_text(answer)}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def render_ingestion_status(success: bool, name: str):
    if success:
        st.markdown(
            f"""
            <div class="ingest-toast">✓ {_safe(name)} added to Louda AI</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="ingest-toast error">✗ Failed to ingest {_safe(name)}</div>
            """,
            unsafe_allow_html=True,
        )


# ---- app runtime ----

st.set_page_config(
    page_title="Louda AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

try:
    validate_config()
except ValueError as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ingested" not in st.session_state:
    st.session_state.ingested = set()

    docs_dir = Path("docs")
    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.*"):
            if doc_file.suffix.lower() not in (".txt", ".md", ".pdf"):
                continue
            try:
                docs, name = load_document(str(doc_file))
                chunks = chunk_documents(docs)
                for chunk in chunks:
                    chunk.metadata["source"] = doc_file.name
                add_documents(chunks)
                st.session_state.ingested.add(doc_file.name)
            except Exception as e:
                st.warning(f"Could not auto-ingest {doc_file.name}: {e}")

uploaded_files = render_sidebar()

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.ingested:
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            try:
                docs, _ = load_document(tmp_path)
                chunks = chunk_documents(docs)
                for chunk in chunks:
                    chunk.metadata["source"] = uploaded_file.name
                success = add_documents(chunks)
                render_ingestion_status(success, uploaded_file.name)
                if success:
                    st.session_state.ingested.add(uploaded_file.name)
            except Exception as e:
                st.error(f"Could not process {uploaded_file.name}: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

doc_count = count_documents()

if not st.session_state.messages:
    render_welcome(doc_count=doc_count)
    if doc_count == 0:
        render_empty_state()

for message in st.session_state.messages:
    if message["role"] == "user":
        render_user_message(message["content"])
    else:
        render_answer(message.get("answer", "Louda hasn't shared that with me yet."))

if prompt := st.chat_input("Ask anything from the knowledge base..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_user_message(prompt)

    if count_documents() == 0:
        answer = "Louda hasn't shared that with me yet. Upload Louda's profile, notes, or project documents first."
        sources = []
    else:
        with st.spinner(""):
            result = ask(prompt)
        answer = result.get("answer", result.get("response", "Louda hasn't shared that with me yet."))
        sources = result.get("sources", result.get("source_documents", []))

    st.session_state.messages.append({"role": "assistant", "answer": answer})
    render_answer(answer)
