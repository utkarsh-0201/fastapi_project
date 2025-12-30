from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    Represents an application user.

    - Auto-incrementing integer primary key
    - Email-based authentication
    - Soft-delete and activation support
    """

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------
    user_id: int = Field(
        default=None,
        primary_key=True,
        index=True,
        description="Auto-incrementing user identifier",
    )

    # ------------------------------------------------------------------
    # Authentication & Identity
    # ------------------------------------------------------------------
    email: str = Field(
        index=True,
        unique=True,
        nullable=False,
        description="User email address (unique)",
    )

    hashed_password: str = Field(
        nullable=False,
        description="Hashed user password",
    )

    # ------------------------------------------------------------------
    # User status & access control
    # ------------------------------------------------------------------
    is_active: bool = Field(
        default=True,
        nullable=False,
        description="Whether the user account is active",
    )

    is_superuser: bool = Field(
        default=False,
        nullable=False,
        description="Grants admin-level access",
    )

    # ------------------------------------------------------------------
    # sa_column: It’s a way to directly define the Column when SQLModel’s Field() is not expressive enough,
    # typically for server-side defaults, timestamps, database-specific types, or advanced constraints.
    # ------------------------------------------------------------------
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        description="User creation timestamp",
    )

    last_login_at: Optional[datetime] = Field(
        default=None,
        description="Last successful login timestamp",
    )
