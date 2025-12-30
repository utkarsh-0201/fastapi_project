"""Centralized logging configuration."""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    """Configure application logging and sanity-check some settings."""
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Warn if running with the default insecure secret
    if settings.secret_key == "dev-secret-key-change-in-production":
        logging.getLogger("app").warning(
            "Using default SECRET_KEY; set a secure SECRET_KEY in production"
        )


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)
