"""Currency API schemas."""

from pydantic import BaseModel


class CurrencyCreate(BaseModel):
    """Schema for creating currencies."""

    currency_id: str
    name: str
    is_active: bool = True

    class ConfigDict:
        json_schema_extra = {
            "example": {"currency_id": "USD", "name": "US Dollar", "is_active": True}
        }


class CurrencyResponse(BaseModel):
    """Schema for currency responses."""

    currency_id: str
    name: str
    is_active: bool

    class ConfigDict:
        from_attributes = True
