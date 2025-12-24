"""Expense API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query, status
from sqlmodel import select

from app.core.logging import get_logger
from app.db.engine import SessionDep
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse

logger = get_logger(__name__)
router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=list[ExpenseResponse], summary="Get all expenses")
def get_all_expenses(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Expense]:
    """Get all expenses."""
    logger.info("Fetching all expenses")
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()

    if not expenses:
        logger.info("No expenses found")
        return []

    logger.info(f"Found {len(expenses)} expenses")
    return list(expenses)


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create expense",
)
def create_expense(session: SessionDep, expense_data: ExpenseCreate) -> Expense:
    """Create a new expense."""
    expense = Expense(**expense_data.model_dump())
    session.add(expense)
    session.commit()
    session.refresh(expense)

    logger.info(f"Created expense {expense.id}")
    return expense


@router.get("/{expense_id}", response_model=ExpenseResponse, summary="Get expense by ID")
def get_expense(
    session: SessionDep, expense_id: UUID = Path(..., description="Expense ID")
) -> Expense:
    """Get expense by ID."""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    return expense


# @router.put(
#     "/{expense_id}",
#     response_model=ExpenseResponse,
#     summary="Update expense"
# )
# def update_expense(
#     session: SessionDep,
#     expense_id: UUID,
#     expense_data: ExpenseUpdate
# ) -> Expense:
#     """Update an expense."""
#     expense = session.get(Expense, expense_id)
#     if not expense:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Expense not found"
#         )

#     for field, value in expense_data.model_dump().items():
#         setattr(expense, field, value)

#     session.add(expense)
#     session.commit()
#     session.refresh(expense)

#     logger.info(f"Updated expense {expense_id}")
#     return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete expense")
def delete_expense(session: SessionDep, expense_id: UUID) -> None:
    """Delete an expense."""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    session.delete(expense)
    session.commit()

    logger.info(f"Deleted expense {expense_id}")
