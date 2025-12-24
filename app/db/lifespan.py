"""Database lifespan management."""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.core.logging import get_logger
from app.db.engine import engine

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Manage database lifecycle."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")
    yield
    logger.info("Application shutdown")
