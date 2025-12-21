"""FastAPI Expense Tracker API

A simple expense tracking API that allows users to manage their expenses
with CRUD operations and category filtering.

This module contains the main FastAPI application and all route handlers.
"""

from __future__ import annotations

import logging
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ExpenseBase(BaseModel):
    """Base model for expense data validation."""

    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(
        ..., min_length=1, max_length=50, description="Expense category"
    )
    currency: str = Field(
        ...,
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code (e.g., INR, USD)",
    )
    vendor: str = Field(
        ..., min_length=1, max_length=100, description="Vendor or merchant name"
    )

    # Field validators - automatically clean and normalize data during model creation
    # These run whenever an ExpenseBase model is instantiated (create/update operations)

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        """Normalize category to lowercase and strip whitespace.

        Example: "  FOOD  " becomes "food"
        """
        return value.strip().lower()

    @field_validator("vendor")
    @classmethod
    def normalize_vendor(cls, value: str) -> str:
        """Normalize vendor name by stripping whitespace.

        Example: "  McDonald's  " becomes "McDonald's"
        """
        return value.strip()


class Expense(ExpenseBase):
    """Complete expense model with auto-generated ID."""

    id: UUID = Field(default_factory=uuid4, description="Unique expense identifier")

    class ConfigDict:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "amount": 25.50,
                "category": "food",
                "currency": "INR",
                "vendor": "McDonald's",
            }
        }


class ExpenseCreate(ExpenseBase):
    """Model for creating new expenses (without ID)."""

    class ConfigDict:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "amount": 25.50,
                "category": "food",
                "currency": "INR",
                "vendor": "McDonald's",
            }
        }


class ExpenseUpdate(ExpenseBase):
    """Model for updating existing expenses."""

    pass


# FastAPI application instance
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="A simple expense tracking API with CRUD operations and filtering",
    docs_url="/docs",
    redoc_url="/redoc",
)

# In-memory storage - Replace with database in production
EXPENSES_BY_USER: dict[str, list[Expense]] = {
    "123": [
        Expense(amount=10.5, category="food", currency="INR", vendor="Swiggy"),
        Expense(amount=120.0, category="transportation", currency="INR", vendor="Uber"),
        Expense(amount=120.0, category="transportation", currency="INR", vendor="Uber"),
        Expense(amount=10.5, category="food", currency="INR", vendor="Swiggy"),
    ],
    "124": [
        Expense(amount=1500.0, category="shopping", currency="INR", vendor="Amazon"),
        Expense(
            amount=300.0, category="entertainment", currency="INR", vendor="BookMyShow"
        ),
    ],
    "125": [
        Expense(amount=250.0, category="food", currency="INR", vendor="Zomato"),
    ],
    "126": [
        Expense(
            amount=1200.0,
            category="utilities",
            currency="INR",
            vendor="Electricity Board",
        ),
        Expense(
            amount=799.0, category="subscription", currency="INR", vendor="Netflix"
        ),
    ],
    "127": [
        Expense(amount=450.0, category="health", currency="INR", vendor="PharmEasy"),
    ],
}


def get_user_expenses_from_storage(user_id: str) -> list[Expense]:
    """Retrieve user expenses from storage.

    Args:
        user_id: The user identifier

    Returns:
        list of expenses for the user

    Raises:
        HTTPException: If user is not found
    """
    if user_id not in EXPENSES_BY_USER:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found",
        )
    return EXPENSES_BY_USER[user_id]


def filter_expenses_by_category(
    expenses: list[Expense], category: str | None = None
) -> list[Expense]:
    """Filter expenses by category.

    Args:
        expenses: list of expenses to filter
        category: Category to filter by (case-insensitive)

    Returns:
        Filtered list of expenses
    """
    if not category:
        return expenses

    normalized_category = category.strip().lower()
    filtered = [
        expense for expense in expenses if expense.category == normalized_category
    ]

    logger.info(
        f"Filtered {len(filtered)} expenses for category: {normalized_category}"
    )
    return filtered


def find_expense_by_id(expenses: list[Expense], expense_id: UUID) -> Expense | None:
    """Find an expense by its ID.

    Args:
        expenses: list of expenses to search
        expense_id: UUID of the expense to find

    Returns:
        The expense if found, None otherwise
    """
    for expense in expenses:
        if expense.id == expense_id:
            return expense
    return None


@app.get(
    "/",
    response_model=dict[str, list[Expense]],
    status_code=status.HTTP_200_OK,
    summary="Get all expenses for all users",
    description="Retrieve all expenses across all users. Useful for admin purposes.",
    tags=["expenses"],
)
def get_all_expenses() -> dict[str, list[Expense]]:
    """Get all expenses for all users.

    Returns:
        Dictionary mapping user IDs to their expense lists
    """
    logger.info("Fetching all expenses for all users")
    return EXPENSES_BY_USER


@app.get(
    "/expenses/{user_id}",
    response_model=list[Expense],
    status_code=status.HTTP_200_OK,
    summary="Get expenses for a specific user",
    description="Retrieve all expenses for a user, optionally filtered by category.",
    tags=["expenses"],
)
def get_user_expenses(
    user_id: str = Path(..., description="User ID to fetch expenses for"),
    category: str | None = Query(
        default=None, description="Filter expenses by category (case-insensitive)", min_length=1
    ),
) -> list[Expense]:
    """Get expenses for a specific user with optional category filtering.

    Args:
        user_id: The user identifier
        category: Optional category filter

    Returns:
        list of expenses for the user

    Raises:
        HTTPException: If user is not found
    """
    expenses = get_user_expenses_from_storage(user_id)
    filtered_expenses = filter_expenses_by_category(expenses, category)

    logger.info(
        f"Retrieved {len(filtered_expenses)} expenses for user {user_id}"
        f"{f' in category {category}' if category else ''}"
    )

    return filtered_expenses


@app.post(
    "/expenses/{user_id}",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new expense for a user",
    description="Create a new expense entry for the specified user.",
    tags=["expenses"],
)
def add_expense(
    expense_data: ExpenseCreate,
    user_id: str = Path(..., description="User ID to add expense for")
) -> Expense:
    """Add a new expense for a user.

    Args:
        user_id: The user identifier
        expense_data: Expense data to create

    Returns:
        The created expense with generated ID

    Raises:
        HTTPException: If user is not found
    """
    # Ensure user exists
    get_user_expenses_from_storage(user_id)

    # Create expense with auto-generated ID
    expense = Expense(**expense_data.model_dump())
    EXPENSES_BY_USER[user_id].append(expense)

    logger.info(
        f"Added expense {expense.id} for user {user_id}: "
        f"{expense.amount} {expense.currency} at {expense.vendor}"
    )

    return expense


@app.put(
    "/expenses/{user_id}/{expense_id}",
    response_model=Expense,
    status_code=status.HTTP_200_OK,
    summary="Update an existing expense",
    description="Update all fields of an existing expense.",
    tags=["expenses"],
)
def update_expense(
    expense_data: ExpenseUpdate,
    user_id: str = Path(..., description="User ID who owns the expense"),
    expense_id: UUID = Path(..., description="Expense ID to update"),
) -> Expense:
    """Update an existing expense.

    Args:
        user_id: The user identifier
        expense_id: The expense identifier
        expense_data: Updated expense data

    Returns:
        The updated expense

    Raises:
        HTTPException: If user or expense is not found
    """
    expenses = get_user_expenses_from_storage(user_id)
    expense = find_expense_by_id(expenses, expense_id)

    if not expense:
        logger.warning(f"Expense {expense_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID '{expense_id}' not found",
        )

    # Update all fields
    expense.amount = expense_data.amount
    expense.category = expense_data.category
    expense.currency = expense_data.currency
    expense.vendor = expense_data.vendor

    logger.info(f"Updated expense {expense_id} for user {user_id}")
    return expense


@app.delete(
    "/expenses/{user_id}/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
    description="Remove an expense from the user's expense list.",
    tags=["expenses"],
)
def delete_expense(
    user_id: str = Path(..., description="User ID who owns the expense"),
    expense_id: UUID = Path(..., description="Expense ID to delete"),
) -> None:
    """Delete an existing expense.

    Args:
        user_id: The user identifier
        expense_id: The expense identifier

    Raises:
        HTTPException: If user or expense is not found
    """
    expenses = get_user_expenses_from_storage(user_id)
    expense = find_expense_by_id(expenses, expense_id)

    if not expense:
        logger.warning(f"Expense {expense_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID '{expense_id}' not found",
        )

    EXPENSES_BY_USER[user_id].remove(expense)
    logger.info(f"Deleted expense {expense_id} for user {user_id}")
