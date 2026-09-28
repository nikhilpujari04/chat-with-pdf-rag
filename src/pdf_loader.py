"""
Handles extraction of text from uploaded PDF files.
Each page's text is kept separate, tagged with its page number,
so later steps (chunking, citation) can trace content back to its source page.
"""

from pypdf import PdfReader
from src.logger import get_logger

logger = get_logger(__name__)


def load_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from a PDF, page by page.

    Args:
        file_path: Path to the PDF file on disk.

    Returns:
        A list of dicts, one per page:
        [{"page_number": 1, "text": "..."}, {"page_number": 2, "text": "..."}, ...]
        Pages with no extractable text (e.g. blank or scanned) are skipped.
    """
    logger.info(f"Loading PDF: {file_path}")

    try:
        reader = PdfReader(file_path)
    except Exception as e:
        logger.error(f"Failed to open PDF '{file_path}': {e}")
        raise ValueError(f"Could not open PDF file: {e}")

    pages_data = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text()
        except Exception as e:
            logger.warning(f"Failed to extract text from page {page_number}: {e}")
            continue

        if text and text.strip():
            pages_data.append({
                "page_number": page_number,
                "text": text.strip()
            })
        else:
            logger.warning(f"Page {page_number} has no extractable text (possibly scanned/image-based).")

    if not pages_data:
        logger.error(f"No extractable text found in '{file_path}'.")
        raise ValueError("No text could be extracted from this PDF. It may be a scanned/image-based document.")

    logger.info(f"Successfully extracted text from {len(pages_data)} page(s) of '{file_path}'.")
    return pages_data