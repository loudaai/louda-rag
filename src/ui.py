import html

import streamlit as st

from src.prompts import EMPTY_UPLOAD_TEXT, WELCOME_TEXT
from src.vector_store import count_documents


def _safe(value: str) -> str:
    return html.escape(str(value or ""))


def _format_text(value: str) -> str:
    return _safe(value).replace("\n", "<br>")


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        :root {
            --bg: #0c0c0f;
            --ink: #f4f4f5;
            --muted: #a0a0a8;
            --faint: #8a8a92;
            --surface: #18181b;
            --surface-2: #1e1e22;
            --line: #2a2a30;
            --line-strong: #3a3a42;
            --danger: #ef4444;
        }

        * {
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        html,
        body,
        [class*="css"] {
            background: var(--bg) !important;
            color: var(--ink) !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top center, rgba(255,255,255,0.05), transparent 34rem),
                linear-gradient(180deg, #0c0c0f 0%, #09090b 100%);
            color: var(--ink);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: 0.16;
            background-image: radial-gradient(circle, rgba(244,244,245,0.42) 1px, transparent 1px);
            background-size: 9px 9px;
            mask-image: radial-gradient(circle at 50% 0%, black 0%, transparent 48%);
            -webkit-mask-image: radial-gradient(circle at 50% 0%, black 0%, transparent 48%);
            z-index: 0;
        }

        .block-container {
            position: relative;
            z-index: 1;
            max-width: 820px !important;
            padding: 2.25rem 1rem 8rem !important;
            margin: 0 auto !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        div[data-testid="stToolbar"] {
            display: none !important;
        }

        #MainMenu,
        footer {
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
            padding: 4.4rem 0 2.1rem;
            animation: fadeUp 700ms cubic-bezier(0.16, 1, 0.3, 1) both;
        }

        .hero h1 {
            margin: 0;
            font-size: clamp(2.25rem, 7vw, 4.2rem);
            line-height: 0.95;
            letter-spacing: -0.075em;
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
            border-radius: 18px 18px 5px 18px;
            padding: 0.72rem 1rem;
            font-size: 14px;
            line-height: 1.55;
            box-shadow: 0 18px 40px -26px rgba(0,0,0,0.75);
        }

        .answer-card {
            position: relative;
            border: 1px solid var(--line);
            border-radius: 20px;
            background: rgba(24,24,27,0.72);
            padding: 1.35rem;
            margin: 0 0 1.2rem;
            box-shadow: 0 22px 50px -36px rgba(0,0,0,0.95);
            animation: fadeUp 420ms cubic-bezier(0.16, 1, 0.3, 1) both;
            overflow: hidden;
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

        .answer-content {
            color: var(--ink);
            font-size: 15px;
            line-height: 1.78;
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

        /* ---------- Streamlit bottom area ---------- */

        div[data-testid="stBottomBlockContainer"],
        div[data-testid="stBottom"] {
            background: linear-gradient(180deg, rgba(12,12,15,0), rgba(12,12,15,0.96) 32%) !important;
            padding-top: 1rem !important;
        }

        /* ---------- ChatGPT/OpenAI-style input ---------- */

        div[data-testid="stChatInput"] {
            position: relative !important;
            width: min(820px, calc(100vw - 2rem)) !important;
            max-width: 820px !important;
            margin: 0 auto !important;
            padding: 0 0 1rem 0 !important;
            background: transparent !important;
        }

        /*
        Streamlit versions differ. Some use a form; some use nested divs.
        Style both so the input always becomes a compact rounded composer.
        */
        div[data-testid="stChatInput"] > div,
        div[data-testid="stChatInput"] form {
            position: relative !important;
            display: flex !important;
            align-items: center !important;

            min-height: 58px !important;
            max-height: 180px !important;

            padding: 0.45rem 3.35rem 0.45rem 1.05rem !important;

            background: #18181b !important;
            border: 1px solid #2a2a30 !important;
            border-radius: 999px !important;

            box-shadow: 0 18px 50px -38px rgba(0,0,0,0.95) !important;
            outline: none !important;
        }

        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatInput"] [data-baseweb="base-input"] {
            width: 100% !important;
            flex: 1 1 auto !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 0 !important;
        }

        div[data-testid="stChatInput"] textarea {
            width: 100% !important;
            min-height: 28px !important;
            max-height: 130px !important;

            padding: 0.42rem 0 !important;
            margin: 0 !important;

            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;

            color: #f4f4f5 !important;
            font-size: 15px !important;
            line-height: 1.5 !important;

            resize: none !important;
        }

        div[data-testid="stChatInput"] textarea:focus,
        div[data-testid="stChatInput"] textarea:focus-visible,
        div[data-testid="stChatInput"] textarea:active,
        div[data-testid="stChatInput"] [data-baseweb="textarea"]:focus,
        div[data-testid="stChatInput"] [data-baseweb="textarea"]:focus-within,
        div[data-testid="stChatInput"] [data-baseweb="base-input"]:focus-within {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: #8a8a92 !important;
            opacity: 0.88 !important;
        }

        div[data-testid="stChatInput"] button,
        button[data-testid="stChatInputSubmitButton"] {
            position: absolute !important;
            right: 10px !important;
            top: 50% !important;
            bottom: auto !important;
            transform: translateY(-50%) !important;

            width: 38px !important;
            height: 38px !important;
            min-width: 38px !important;

            margin: 0 !important;
            padding: 0 !important;

            border: none !important;
            border-radius: 999px !important;

            background: #f4f4f5 !important;
            color: #0c0c0f !important;

            display: flex !important;
            align-items: center !important;
            justify-content: center !important;

            box-shadow: none !important;
            cursor: pointer !important;
            z-index: 50 !important;
            transition: opacity 160ms ease, transform 160ms ease !important;
        }

        div[data-testid="stChatInput"] button:hover,
        button[data-testid="stChatInputSubmitButton"]:hover {
            opacity: 0.86 !important;
            transform: translateY(-50%) scale(1.03) !important;
        }

        div[data-testid="stChatInput"] button:disabled,
        button[data-testid="stChatInputSubmitButton"]:disabled {
            background: #3a3a42 !important;
            opacity: 0.45 !important;
            cursor: default !important;
        }

        div[data-testid="stChatInput"] button svg,
        button[data-testid="stChatInputSubmitButton"] svg {
            width: 17px !important;
            height: 17px !important;
            fill: #0c0c0f !important;
            color: #0c0c0f !important;
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
                max-width: 100% !important;
                padding: 1.15rem 1rem 7.5rem !important;
            }

            .hero {
                padding: 2.15rem 0 1.65rem !important;
            }

            .hero h1 {
                font-size: 2.05rem !important;
                line-height: 1 !important;
                letter-spacing: -0.06em !important;
            }

            .hero-sub {
                max-width: 21rem !important;
                margin-top: 0.85rem !important;
                font-size: 14px !important;
                line-height: 1.55 !important;
            }

            .thread {
                margin-top: 0.5rem !important;
            }

            .user-message {
                margin-bottom: 0.85rem !important;
                padding-left: 2rem !important;
            }

            .user-bubble {
                max-width: 86% !important;
                border-radius: 18px 18px 5px 18px !important;
                padding: 0.65rem 0.9rem !important;
                font-size: 14px !important;
                line-height: 1.5 !important;
            }

            .answer-card {
                border-radius: 18px !important;
                padding: 1rem !important;
                margin-bottom: 1rem !important;
                box-shadow: none !important;
            }

            .answer-topline {
                margin-bottom: 0.65rem !important;
            }

            .answer-label {
                font-size: 9px !important;
            }

            .answer-content {
                font-size: 15px !important;
                line-height: 1.65 !important;
            }

            div[data-testid="stChatInput"] {
                width: calc(100vw - 1.2rem) !important;
                max-width: calc(100vw - 1.2rem) !important;
                padding-bottom: 0.75rem !important;
            }

            div[data-testid="stChatInput"] > div,
            div[data-testid="stChatInput"] form {
                min-height: 54px !important;
                border-radius: 999px !important;
                padding: 0.4rem 3rem 0.4rem 1rem !important;
            }

            div[data-testid="stChatInput"] textarea {
                min-height: 26px !important;
                max-height: 110px !important;
                font-size: 14px !important;
                padding: 0.4rem 0 !important;
            }

            div[data-testid="stChatInput"] button,
            button[data-testid="stChatInputSubmitButton"] {
                width: 34px !important;
                height: 34px !important;
                min-width: 34px !important;
                right: 9px !important;
            }

            div[data-testid="stChatInput"] button svg,
            button[data-testid="stChatInputSubmitButton"] svg {
                width: 15px !important;
                height: 15px !important;
            }
        }

        @media (max-width: 480px) {
            .hero h1 {
                font-size: 2rem !important;
            }

            .hero-sub {
                font-size: 13px !important;
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

        st.markdown(
            '<div class="micro-label">upload knowledge</div>',
            unsafe_allow_html=True,
        )

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
            <h1>Ask About Louda</h1>
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
