from typing import List, Optional

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from src.config import CHROMA_DIR, EMBEDDING_MODEL, TOP_K


_embeddings = None
_db = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings


def _get_db(collection_name="louda_docs"):
    global _db
    if _db is None:
        _db = Chroma(
            collection_name=collection_name,
            embedding_function=_get_embeddings(),
            persist_directory=str(CHROMA_DIR),
        )
    return _db


def add_documents(docs: List[Document]) -> bool:
    db = _get_db()
    try:
        db.add_documents(docs)
        print(f"Documents successfully added to ChromaDB at {CHROMA_DIR}")
        return True
    except Exception as e:
        print(f"Failed to add documents to ChromaDB: {e}")
        return False


def search(query: str, k: int = TOP_K) -> List[Document]:
    db = _get_db()
    results = db.similarity_search(query, k=k)
    return results


def count_documents() -> int:
    db = _get_db()
    return db._collection.count()


def delete_all():
    try:
        db = _get_db()
        db.delete_collection()
        global _db
        _db = None
        return True
    except Exception as e:
        print(f"Failed to delete collection: {e}")
        return False
