
from sqlmodel import SQLModel


class ExpenseCreate(SQLModel):
    """
    Client sends currency code, not currency_id.
    API converts it internally.
    """

    amount: float
    category: str
    vendor: str
    currency_id: str


class ExpenseUpdate(SQLModel):
    amount: float | None = None
    category: str | None = None
    vendor: str | None = None
    currency: str | None = None


class ExpenseResponse(SQLModel):
    id: int
    amount: float
    category: str
    vendor: str
    currency_id: str
