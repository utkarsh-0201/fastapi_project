"""
Expense API routes.

This module contains CRUD operations for expenses.
All endpoints are protected and scoped to the authenticated user.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select

from app.core.dependencies import get_current_user
from app.core.logging import get_logger
from app.db.engine import SessionDep
from app.models.expense import Expense
from app.models.user import User
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseUpdate,
)

logger = get_logger(__name__)

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
    dependencies=[Depends(get_current_user)],  # authentication enforced globally
)

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------


def get_expense_or_404(
    session: SessionDep,
    expense_id: int,
    user_id: int,
) -> Expense:
    """
    Fetch an expense owned by the given user or raise 404.

    This ensures user ownership (authorization).
    """
    expense = session.exec(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id,
        )
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        ) from None

    return expense


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

@router.get(
    "/",
    response_model=list[ExpenseResponse],
    summary="Get all expenses for current user",
)
def get_all_expenses(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 100,
) -> list[Expense]:
    """
    Retrieve all expenses belonging to the authenticated user.

    Supports pagination using offset and limit.
    """
    logger.info("Fetching expenses for user %s", current_user.email)

    expenses = list(session.exec(
        select(Expense)
        .where(Expense.user_id == str(current_user.user_id))
        .offset(offset)
        .limit(limit)
    ).all())

    return expenses


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
)
def create_expense(
    session: SessionDep,
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
) -> Expense:
    """
    Create a new expense for the authenticated user.
    """
    try:
        expense = Expense(
            **expense_data.model_dump(),
            user_id=str(current_user.user_id),  # ownership enforced at creation
        )
        session.add(expense)
        session.commit()
        session.refresh(expense)

        logger.info(
            "Created expense %s for user %s",
            expense.id,
            current_user.email,
        )
        return expense

    except Exception:
        session.rollback()
        logger.exception("Failed to create expense")
        raise


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Get expense by ID",
)
def get_expense(
    session: SessionDep,
    expense_id: int,
    current_user: User = Depends(get_current_user),
) -> Expense:
    """
    Retrieve a single expense by ID.

    Only expenses owned by the authenticated user are accessible.
    """
    return get_expense_or_404(session, expense_id, current_user.user_id)


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
    summary="Update an expense",
)
def update_expense(
    session: SessionDep,
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
) -> Expense:
    """
    Update an existing expense.

    - Only the owner can update the expense
    - Supports partial updates
    """
    expense = get_expense_or_404(session, expense_id, current_user.user_id)

    try:
        update_data = expense_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(expense, field, value)

        session.add(expense)
        session.commit()
        session.refresh(expense)

        logger.info(
            "Updated expense %s for user %s",
            expense_id,
            current_user.user_id,
        )
        return expense

    except Exception:
        session.rollback()
        logger.exception("Failed to update expense %s", expense_id)
        raise


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
)
def delete_expense(
    session: SessionDep,
    expense_id: int,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete an expense owned by the authenticated user.
    """
    expense = get_expense_or_404(session, expense_id, current_user.user_id)

    try:
        session.delete(expense)
        session.commit()

        logger.info(
            "Deleted expense %s for user %s",
            expense_id,
            current_user.user_id,
        )
        return None

    except Exception:
        session.rollback()
        logger.exception("Failed to delete expense %s", expense_id)
        raise
