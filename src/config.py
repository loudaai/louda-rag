import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"
DOCS_DIR = BASE_DIR / "docs"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-70b-8192"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K = 4
MAX_TOKENS = 512
TEMPERATURE = 0.3

def validate_config():
    if not GROQ_API_KEY:
        raise ValueError(
            "The app could not find your Groq API key. "
            "Add GROQ_API_KEY to .env locally or Streamlit Secrets in production."
        )
