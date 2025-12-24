from __future__ import annotations

from datetime import datetime

# from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel

# if TYPE_CHECKING:
#     from app.models.expense import Expense


class User(SQLModel, table=True):
    """
    Represents an application user.

    At this stage, the user model is intentionally minimal.
    Authentication and profile details can be added later
    without changing the Expense schema.
    """

    # Primary identifier for the user
    # Using string instead of integer allows flexibility
    # (UUID, email, external auth ID, etc.)
    user_id: str = Field(primary_key=True, index=True, description="Unique user identifier")

    # Audit fields — extremely useful in production
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False, description="User creation timestamp"
    )

    is_active: bool = Field(default=True, description="Soft delete / disable flag")

    # Relationship to expenses
    # Not stored as a column — only used by ORM
    # expenses: List["Expense"] = Relationship(
    #     back_populates="user"
    # )
