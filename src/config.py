"""
Centralized configuration for the RAG application.
All environment variables and app-wide settings are defined here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # --- API Keys ---
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # --- LLM Settings ---
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

    # --- Embedding Settings ---
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # --- Chunking Settings ---
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 100

    # --- File Paths ---
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")
    VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "data/vector_store")
    VECTOR_STORE_PATH = os.getenv(
        "VECTOR_STORE_PATH",
        os.path.join(VECTOR_STORE_DIR, "index")
    )
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_FILE = os.getenv("LOG_FILE", os.path.join(LOG_DIR, "app.log"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls):
        """Check that required settings are present. Fail early and clearly."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is missing. Please add it to your .env file."
            )




def get_config():
    """Return the config class for application use."""
    return Config


# Run validation as soon as this module is imported
Config.validate()