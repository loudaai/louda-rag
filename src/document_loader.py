from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def load_document(file_path: str) -> Tuple[List[Document], str]:
    path = Path(file_path)
    suffix = path.suffix.lower()
    name = path.name

    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()
    elif suffix in (".txt", ".md", ".markdown"):
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    raw_text = " ".join(d.page_content for d in docs)
    total_chars = len(raw_text)

    print(f"File: {name}")
    print(f"Raw pages/docs loaded: {len(docs)}")
    print(f"Total extracted characters: {total_chars}")
    print(f"First 300 chars: {raw_text[:300]}")

    return docs, name


def chunk_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )
    chunks = splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    print(f"Chunks created: {len(chunks)}")
    return chunks
