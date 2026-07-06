import streamlit as st
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

from src.config import validate_config
from src.document_loader import load_document, chunk_documents
from src.vector_store import add_documents, count_documents
from src.rag import ask
from src.ui import (
    inject_css,
    render_header,
    render_sidebar,
    render_welcome,
    render_empty_state,
    render_answer,
    render_ingestion_status,
)

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
            if doc_file.suffix.lower() in (".txt", ".md", ".pdf"):
                try:
                    docs, name = load_document(str(doc_file))
                    chunks = chunk_documents(docs)
                    for chunk in chunks:
                        chunk.metadata["source"] = name
                    add_documents(chunks)
                    st.session_state.ingested.add(name)
                except Exception as e:
                    st.warning(f"Could not auto-ingest {doc_file.name}: {e}")

uploaded_files = render_sidebar()
doc_count = count_documents()

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.ingested:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=Path(uploaded_file.name).suffix
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                docs, name = load_document(tmp_path)
                chunks = chunk_documents(docs)
                for chunk in chunks:
                    chunk.metadata["source"] = uploaded_file.name
                success = add_documents(chunks)
                render_ingestion_status(success, uploaded_file.name)
            except Exception as e:
                st.error(f"Could not process {uploaded_file.name}: {e}")
            finally:
                os.unlink(tmp_path)

            st.session_state.ingested.add(uploaded_file.name)
            doc_count = count_documents()

if doc_count == 0 and not st.session_state.messages:
    render_welcome()
    render_empty_state()
elif doc_count > 0 and not st.session_state.messages:
    render_welcome()

for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message fade-in">
            <div class="bubble">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            render_answer(
                message["answer"],
                message.get("sources", []),
                message.get("chunks", []),
            )

if prompt := st.chat_input("Ask Louda AI a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown(f"""
    <div class="user-message fade-in">
        <div class="bubble">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner(""):
            result = ask(prompt)
            render_answer(
                result["answer"],
                result["sources"],
                result["chunks"],
            )

    st.session_state.messages.append({
        "role": "assistant",
        "answer": result["answer"],
        "sources": result["sources"],
        "chunks": result["chunks"],
    })

    st.rerun()
