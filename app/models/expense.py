from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class ExpenseBase(SQLModel):
    amount: float = Field(gt=0)
    category: str
    vendor: str

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        """Normalize category to lowercase."""
        return value.strip().lower()

    @field_validator("vendor")
    @classmethod
    def normalize_vendor(cls, value: str) -> str:
        """Normalize vendor name."""
        return value.strip()


class Expense(ExpenseBase, table=True):
    """Expense table with foreign key references."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.user_id", index=True)
    currency_id: str = Field(foreign_key="currency.currency_id", index=True)
