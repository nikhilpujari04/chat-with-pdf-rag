"""
Provides the embedding model used to convert text chunks into vectors.
Uses a local HuggingFace sentence-transformer model — no API calls,
no per-request cost, runs on CPU.
"""
import os
os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"

from langchain_huggingface import HuggingFaceEmbeddings
from src.config import Config
from src.logger import get_logger

logger = get_logger(__name__)

_embedding_model = None  # cached singleton, loaded only once per run


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Returns a cached instance of the embedding model.
    Loading the model is relatively slow (a few seconds), so we load it
    once and reuse it rather than reloading on every call.
    """
    global _embedding_model

    if _embedding_model is None:
        logger.info(f"Loading embedding model: {Config.EMBEDDING_MODEL}")
        try:
            _embedding_model = HuggingFaceEmbeddings(
                model_name=Config.EMBEDDING_MODEL
            )
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

    return _embedding_model