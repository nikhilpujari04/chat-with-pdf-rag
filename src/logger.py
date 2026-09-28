"""
Centralized logging setup for the RAG application.
Import get_logger() in any module to get a consistent, configured logger.
"""

import logging
import os
from datetime import datetime
from src.config import Config

# Ensure the logs directory exists
os.makedirs(Config.LOG_DIR, exist_ok=True)

# One log file per day, e.g. logs/2026-06-25.log
LOG_FILE = os.path.join(Config.LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure the root logger once
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # also prints to console
    ]
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance scoped to the given module name.
    Usage in any file:
        from src.logger import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Logger setup successful.")
    logger.warning("This is a test warning.")
    logger.error("This is a test error.")
