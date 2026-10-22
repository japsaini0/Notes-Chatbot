import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

RAW_DIR = BASE_DIR / "data" / "raw"
EXTRACTED_DIR = BASE_DIR / "data" / "extracted"
TEXT_DIR = BASE_DIR / "data" / "text"
VECTOR_DIR = BASE_DIR / "vectorstore"

ZIP_NAME = "notes.zip"
COLLECTION_NAME = "notes"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 4
HISTORY_TURNS = 6