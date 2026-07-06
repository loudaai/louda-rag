from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from src.ui import (
    inject_css,
    render_welcome,
    render_empty_state,
    render_answer,
    render_user_message,
)
from src.rag import ask
from src.vector_store import add_documents, count_documents
from src.document_loader import load_document, chunk_documents
from src.config import validate_config


st.set_page_config(
    page_title="Louda AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "ingested" not in st.session_state:
        st.session_state.ingested = set()


def safe_add_documents(chunks) -> bool:
    if not chunks:
        return False

    result = add_documents(chunks)

    if isinstance(result, bool):
        return result

    if isinstance(result, tuple):
        return True

    return result is not False


def auto_ingest_docs_folder() -> None:
    """
    Auto-ingest files from /docs only when the vector DB is empty.
    This avoids duplicate indexing on each Streamlit rerun.
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
            docs, _ = load_document(str(doc_file))
            chunks = chunk_documents(docs)

            for chunk in chunks:
                chunk.metadata["source"] = doc_file.name

            success = safe_add_documents(chunks)

            if success:
                st.session_state.ingested.add(doc_file.name)

        except Exception as e:
            st.warning(f"Could not auto-ingest {doc_file.name}: {e}")


def normalize_rag_result(result) -> str:
    """
    Only return the assistant answer for UI display.
    Sources can still exist internally in src/rag.py,
    but they are not rendered to the user.
    """
    fallback = "Louda hasn't shared that with me yet."

    if isinstance(result, dict):
        return result.get("answer") or result.get("response") or fallback

    if isinstance(result, str):
        return result

    return fallback


def render_history() -> None:
    st.markdown('<div class="thread">', unsafe_allow_html=True)

    for message in st.session_state.messages:
        if message["role"] == "user":
            render_user_message(message["content"])
        else:
            render_answer(
                message.get("answer", "Louda hasn't shared that with me yet.")
            )

    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    try:
        validate_config()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    init_state()
    auto_ingest_docs_folder()

    doc_count = count_documents()

    if not st.session_state.messages:
        render_welcome(doc_count=doc_count)

        if doc_count == 0:
            render_empty_state()

    render_history()

    prompt = st.chat_input("Ask anything")

    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        render_user_message(prompt)

        if count_documents() == 0:
            answer = (
                "Louda hasn't shared that with me yet. "
                "Upload Louda's profile, notes, or project documents first."
            )
        else:
            with st.spinner(""):
                result = ask(prompt)
            answer = normalize_rag_result(result)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "answer": answer,
            }
        )
        render_answer(answer)


if __name__ == "__main__":
    main()
