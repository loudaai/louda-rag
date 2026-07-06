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

uploaded_files = render_sidebar()
render_header()

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.get("ingested", set()):
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

            if "ingested" not in st.session_state:
                st.session_state.ingested = set()
            st.session_state.ingested.add(uploaded_file.name)

doc_count = count_documents()

if doc_count == 0 and not st.session_state.messages:
    render_welcome()
    render_empty_state()
elif doc_count > 0 and not st.session_state.messages:
    render_welcome()

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else None):
        if message["role"] == "assistant":
            render_answer(
                message["answer"],
                message.get("sources", []),
                message.get("chunks", []),
            )
        else:
            st.markdown(message["content"])

if prompt := st.chat_input("Ask Louda AI a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

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
