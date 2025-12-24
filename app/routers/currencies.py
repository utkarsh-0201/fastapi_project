from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.logging import get_logger
from app.db.engine import get_session
from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate, CurrencyResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/", response_model=list[CurrencyResponse])
def list_currencies(session: Session = Depends(get_session)) -> list[Currency]:
    """Get all active currencies."""
    statement = select(Currency).where(Currency.is_active is True)
    return list(session.exec(statement).all())


@router.post("/", response_model=CurrencyResponse, status_code=status.HTTP_201_CREATED)
def create_currency(currency_data: CurrencyCreate, session: Session = Depends(get_session)) -> Currency:
    """Create a new currency."""
    # Check if currency already exists
    existing = session.get(Currency, currency_data.currency_id)
    logger.info(f"Checking Currency existence: {currency_data.currency_id}")
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Currency {currency_data.currency_id} already exists",
        )

    # Create new currency directly
    currency = Currency(
        currency_id=currency_data.currency_id,
        name=currency_data.name,
        is_active=currency_data.is_active,
    )
    session.add(currency)
    session.commit()
    session.refresh(currency)

    return currency
