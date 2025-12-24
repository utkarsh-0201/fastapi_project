"""Database engine and session management."""

from typing import Annotated, Any

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import get_settings

settings = get_settings()

# Database engine
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


def get_session() -> Any:
    """Get database session."""
    with Session(engine) as session:
        yield session


# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]
