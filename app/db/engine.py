"""Database engine and session management."""

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import get_settings

settings = get_settings()

# Database engine
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}

if "sqlite" in settings.database_url:
    engine = create_engine(settings.database_url, connect_args=connect_args)
else:
    engine = create_engine(
        settings.database_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
    )


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for a request, ensuring it's closed afterwards."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]
