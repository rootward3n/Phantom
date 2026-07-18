"""
logger.py
Phantom logging system.
"""

import logging
from logging.handlers import RotatingFileHandler

from config import LOG_DIR, APP_NAME


def get_logger(name: str = "phantom") -> logging.Logger:
    """
    Return a configured Phantom logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = LOG_DIR / "phantom.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("%s logger initialized", APP_NAME)

    return logger
