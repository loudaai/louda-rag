from typing import List, Dict, Tuple

import groq
from langchain_core.documents import Document

from src.config import GROQ_API_KEY, GROQ_MODEL, MAX_TOKENS, TEMPERATURE, TOP_K
from src.prompts import SYSTEM_PROMPT
from src.vector_store import search


_client = None


def _get_client():
    global _client
    if _client is None:
        _client = groq.Groq(api_key=GROQ_API_KEY)
    return _client


def retrieve(query: str, k: int = TOP_K) -> Tuple[List[Document], List[str]]:
    docs = search(query, k=k)
    sources = list(set(d.metadata.get("source", "Unknown") for d in docs if d.metadata))
    return docs, sources


def build_context(docs: List[Document]) -> str:
    context_parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "")
        page_info = f" (page {page})" if page != "" else ""
        context_parts.append(
            f"[Source: {source}{page_info}]\n{doc.page_content}"
        )
    return "\n\n".join(context_parts)


def generate_answer(question: str, context: str) -> str:
    client = _get_client()
    system_prompt = SYSTEM_PROMPT.format(context=context, question=question)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    return response.choices[0].message.content.strip()


def ask(question: str) -> Dict:
    docs, sources = retrieve(question)
    if not docs:
        return {
            "answer": "Louda hasn't shared that with me yet.",
            "sources": [],
            "chunks": [],
        }

    context = build_context(docs)
    answer = generate_answer(question, context)

    chunks = [
        {
            "content": d.page_content[:200],
            "source": d.metadata.get("source", "Unknown"),
            "page": d.metadata.get("page"),
        }
        for d in docs
    ]

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }
