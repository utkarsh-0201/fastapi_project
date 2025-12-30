"""
FastAPI authentication & authorization dependencies.
"""

from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.db.engine import SessionDep
from app.helpers.crud_user import get_user_by_email, get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme)
) -> Any:
    """
    FastAPI dependency:
    - Validates JWT
    - Loads user from DB
    - Ensures user is active
    """
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from None

    user_id: Optional[str] = payload.get("sub")
    email: Optional[str] = payload.get("email")

    if not user_id and not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = None

    if user_id:
        user = get_user_by_id(session, user_id)

    if user is None and email:
        user = get_user_by_email(session, email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user
