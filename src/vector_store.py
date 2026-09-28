"""
Builds, saves, and loads a FAISS vector store from text chunks.
Uses LangChain's Document objects to keep page-number metadata
attached to each chunk, enabling source citation later.
"""

import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embedding_model
from src.config import Config
from src.logger import get_logger
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
logger = get_logger(__name__)


def build_vector_store(chunks: list[dict]) -> FAISS:
    """
    Builds a FAISS vector store from a list of chunk dicts.

    Args:
        chunks: Output from text_splitter.split_into_chunks() —
                 [{"page_number": 1, "chunk_text": "..."}, ...]

    Returns:
        A FAISS vector store object, ready for similarity search.
    """
    logger.info(f"Building vector store from {len(chunks)} chunk(s).")

    documents = [
        Document(
            page_content=chunk["chunk_text"],
            metadata={"page_number": chunk["page_number"]}
        )
        for chunk in chunks
    ]

    embedding_model = get_embedding_model()

    try:
        vector_store = FAISS.from_documents(documents, embedding_model)
    except Exception as e:
        logger.error(f"Failed to build vector store: {e}")
        raise

    logger.info("Vector store built successfully.")
    return vector_store


def save_vector_store(vector_store: FAISS, save_path: str = None) -> None:
    """Saves a FAISS vector store to disk."""
    save_path = save_path or Config.VECTOR_STORE_DIR
    os.makedirs(save_path, exist_ok=True)

    vector_store.save_local(save_path)
    logger.info(f"Vector store saved to '{save_path}'.")


def load_vector_store(save_path: str = None) -> FAISS:
    """Loads a previously saved FAISS vector store from disk."""
    save_path = save_path or Config.VECTOR_STORE_DIR
    embedding_model = get_embedding_model()

    if not os.path.exists(save_path) or not os.listdir(save_path):
        logger.error(f"No vector store found at '{save_path}'.")
        raise FileNotFoundError(f"No vector store found at '{save_path}'. Build one first.")

    try:
        vector_store = FAISS.load_local(
            save_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        logger.error(f"Failed to load vector store from '{save_path}': {e}")
        raise

    logger.info(f"Vector store loaded from '{save_path}'.")
    return vector_store
def build_hybrid_retriever(vector_store: FAISS, chunks: list[dict], k: int = 6):
    """
    Combines semantic (FAISS) search with keyword (BM25) search.
    BM25 catches exact terminology matches that embeddings can under-rank;
    FAISS catches paraphrased/conceptual matches. Their rankings are merged.

    Args:
        vector_store: An existing FAISS vector store.
        chunks: The same chunk dicts used to build the vector store.
        k: How many results each retriever should return before merging.

    Returns:
        An EnsembleRetriever combining both search strategies.
    """
    documents = [
        Document(
            page_content=chunk["chunk_text"],
            metadata={"page_number": chunk["page_number"]}
        )
        for chunk in chunks
    ]

    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = k

    faiss_retriever = vector_store.as_retriever(search_kwargs={"k": k})

    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5]  # equal weight to keyword and semantic ranking
    )

    logger.info("Hybrid retriever (BM25 + FAISS) built successfully.")
    return hybrid_retriever