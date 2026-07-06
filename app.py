from src.ui import (
    inject_css,
    render_sidebar,
    render_welcome,
    render_empty_state,
    render_answer,
    render_user_message,
    render_ingestion_status,
)
from src.rag import ask
from src.vector_store import add_documents, count_documents
from src.document_loader import load_document, chunk_documents
from src.config import validate_config
import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(
    page_title="Louda AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "ingested" not in st.session_state:
        st.session_state.ingested = set()


def safe_add_documents(chunks):
    if not chunks:
        return False

    result = add_documents(chunks)

    if isinstance(result, tuple):
        return True

    return bool(result)


def auto_ingest_docs_folder():
    """
    Auto-ingest files from /docs only when the vector DB is empty.
    This prevents duplicate indexing on every fresh Streamlit session.
    """
    docs_dir = Path("docs")

    if not docs_dir.exists():
        return

    if count_documents() > 0:
        return

    for doc_file in docs_dir.glob("*.*"):
        if doc_file.suffix.lower() not in (".txt", ".md", ".pdf"):
            continue

        try:
            docs, name = load_document(str(doc_file))
            chunks = chunk_documents(docs)

            for chunk in chunks:
                chunk.metadata["source"] = doc_file.name

            success = safe_add_documents(chunks)

            if success:
                st.session_state.ingested.add(doc_file.name)

        except Exception as e:
            st.warning(f"Could not auto-ingest {doc_file.name}: {e}")


def handle_uploads(uploaded_files):
    if not uploaded_files:
        return

    for uploaded_file in uploaded_files:
        if uploaded_file.name in st.session_state.ingested:
            continue

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            docs, _ = load_document(tmp_path)
            chunks = chunk_documents(docs)

            for chunk in chunks:
                chunk.metadata["source"] = uploaded_file.name

            success = safe_add_documents(chunks)
            render_ingestion_status(success, uploaded_file.name)

            if success:
                st.session_state.ingested.add(uploaded_file.name)

        except Exception as e:
            st.error(f"Could not process {uploaded_file.name}: {e}")

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


def normalize_rag_result(result):
    """
    Supports different ask() return shapes:
    - {"answer": "...", "sources": [...]}
    - {"answer": "...", "source_documents": [...]}
    - plain string
    """
    fallback = "Louda hasn't shared that with me yet."

    if isinstance(result, dict):
        answer = result.get("answer") or result.get("response") or fallback
        sources = (
            result.get("sources")
            or result.get("source_documents")
            or result.get("documents")
            or []
        )
        return answer, sources

    if isinstance(result, str):
        return result, []

    return fallback, []


def render_history():
    st.markdown('<div class="thread">', unsafe_allow_html=True)

    for message in st.session_state.messages:
        if message["role"] == "user":
            render_user_message(message["content"])
        else:
            render_answer(
                message.get("answer", "Louda hasn't shared that with me yet."),
                sources=message.get("sources", []),
            )

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    try:
        validate_config()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    init_state()
    auto_ingest_docs_folder()

    uploaded_files = render_sidebar()
    handle_uploads(uploaded_files)

    doc_count = count_documents()

    if not st.session_state.messages:
        render_welcome(doc_count=doc_count)

        if doc_count == 0:
            render_empty_state()

    render_history()

    prompt = st.chat_input("Ask Louda AI anything from the knowledge base...")

    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        render_user_message(prompt)

        if count_documents() == 0:
            answer = "Louda hasn't shared that with me yet. Upload Louda's profile, notes, or project documents first."
            sources = []
        else:
            with st.spinner(""):
                result = ask(prompt)

            answer, sources = normalize_rag_result(result)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "answer": answer,
                "sources": sources,
            }
        )

        render_answer(answer, sources=sources)


if __name__ == "__main__":
    main()
