from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.core.dependencies import get_current_user
from app.core.logging import get_logger
from app.db.engine import SessionDep
from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate, CurrencyResponse

logger = get_logger(__name__)


router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    dependencies=[Depends(get_current_user)]
)


@router.get(
    "/",
    response_model=list[CurrencyResponse],
    summary="Get active currencies",
    status_code=status.HTTP_200_OK,
)
def list_currencies(session: SessionDep) -> list[Currency]:
    logger.info("Fetching active currencies")

    statement = select(Currency).where(Currency.is_active.is_(True))
    currencies = session.exec(statement).all()

    if not currencies:
        logger.info("No active currencies found")
        return []

    logger.info("Found %d active currencies", len(currencies))
    return list(currencies)


@router.post(
    "/",
    response_model=CurrencyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_currency(currency_data: CurrencyCreate, session: SessionDep) -> Currency:
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
