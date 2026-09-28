"""
Splits extracted page text into smaller overlapping chunks,
suitable for embedding. Each chunk retains a reference to its
source page number for later citation.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config
from src.logger import get_logger

logger = get_logger(__name__)


def split_into_chunks(
    pages_data: list[dict],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[dict]:
    """
    Splits page-level text into smaller chunks.

    Args:
        pages_data: Output from pdf_loader.load_pdf() —
                     [{"page_number": 1, "text": "..."}, ...]
        chunk_size: Optional chunk size to override the default.
        chunk_overlap: Optional chunk overlap to override the default.

    Returns:
        A list of chunk dicts:
        [{"page_number": 1, "chunk_text": "..."}, ...]
    """
    chunk_size = chunk_size if chunk_size is not None else Config.CHUNK_SIZE
    chunk_overlap = chunk_overlap if chunk_overlap is not None else Config.CHUNK_OVERLAP

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    all_chunks = []

    for page in pages_data:
        page_chunks = splitter.split_text(page["text"])

        for chunk_text in page_chunks:
            all_chunks.append({
                "page_number": page["page_number"],
                "chunk_text": chunk_text
            })

    logger.info(f"Split {len(pages_data)} page(s) into {len(all_chunks)} chunk(s).")

    if not all_chunks:
        logger.error("No chunks were created from the provided pages.")
        raise ValueError("Text splitting produced no chunks — check the input PDF content.")

    return all_chunks