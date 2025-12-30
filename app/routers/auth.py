from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, verify_password
from app.db.engine import SessionDep
from app.helpers.crud_user import create_user, get_user_by_email
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def register(user_in: UserCreate, session: SessionDep) -> UserRead:
    """
    Register a new user.

    Args:
        user_in (UserCreate): User registration data.
        session (SessionDep): Database session dependency.
    """

    # Basic password policy: enforce minimum length
    if len(user_in.password or "") < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    if get_user_by_email(session, user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = create_user(session, email=user_in.email, password=user_in.password)
    return UserRead(user_id=user.user_id, email=user.email, is_active=user.is_active)


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, str]:
    """
    Authenticate a user and return an access token.

    Args:
        session (SessionDep): Database session dependency.
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.
    """

    user = get_user_by_email(session, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # ------------------------------------------------------------------
    # Update last login timestamp (ONLY after successful auth)
    # ------------------------------------------------------------------
    user.last_login_at = datetime.now(timezone.utc)

    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token(
        subject=str(user.user_id),
        email=user.email,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
