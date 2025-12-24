from sqlmodel import Field, SQLModel


class Currency(SQLModel, table=True):
    """
    Represents an ISO 4217 currency.
    Using the currency code itself as primary key
    because it is globally unique and human-readable.
    """

    currency_id: str = Field(
        primary_key=True,
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code (e.g. INR, USD)",
    )

    name: str = Field(description="Full currency name")
    is_active: bool = Field(default=True)
