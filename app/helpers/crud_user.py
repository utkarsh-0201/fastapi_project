from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.core.security import hash_password
from app.db.engine import SessionDep
from app.models.user import User


def get_user_by_email(session: SessionDep, email: str) -> Any:
    """Return the first user with the given email (case-insensitive)."""
    normalized = email.lower()
    return session.exec(
        select(User).where(User.email == normalized)
    ).first()


def create_user(
    session: SessionDep,
    *,
    email: str,
    password: str,
) -> User:
    """
    Create a new user.

    - Normalizes email
    - Hashes password
    - Handles unique constraint violations
    - Returns persisted User instance
    """
    normalized_email = email.strip().lower()

    user = User(
        email=normalized_email,
        hashed_password=hash_password(password),
        # user_id is auto-generated
        # created_at handled by DB
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        ) from None

    session.refresh(user)
    return user


def get_user_by_id(session: SessionDep, user_id: str) -> Any | None:
    """Fetch a user by primary key. Accepts UUID string or UUID instance."""
    try:
        return session.get(User, user_id)
    except Exception:
        # session.get will raise if invalid type; try returning None
        return None
