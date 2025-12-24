from uuid import UUID

from sqlmodel import SQLModel


class ExpenseCreate(SQLModel):
    """
    Client sends currency code, not currency_id.
    API converts it internally.
    """

    amount: float
    category: str
    vendor: str
    currency: str


class ExpenseResponse(SQLModel):
    id: UUID
    amount: float
    category: str
    vendor: str
    currency: str
