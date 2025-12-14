from __future__ import annotations

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class Expense(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount")
    category: str = Field(..., min_length=1, description="Expense category")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code")
    vendor: str = Field(..., min_length=1, description="Vendor name")
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 10.5,
                "category": "food",
                "currency": "INR",
                "vendor": "Swiggy"
            }
        }

app = FastAPI()

EXPENSES_BY_USER: Dict[str, List[Expense]] = {
    "123": [
        Expense(amount=10.5, category="food", currency="INR", vendor="Swiggy"),
        Expense(amount=120.0, category="transportation", currency="INR", vendor="Uber"),
        Expense(amount=120.0, category="transportation", currency="INR", vendor="Uber"),
        Expense(amount=10.5, category="food", currency="INR", vendor="Swiggy"),
    ],
    "124": [
        Expense(amount=1500.0, category="shopping", currency="INR", vendor="Amazon"),
        Expense(amount=300.0, category="entertainment", currency="INR", vendor="BookMyShow"),
    ],
    "125": [
        Expense(amount=250.0, category="food", currency="INR", vendor="Zomato"),
    ],
    "126": [
        Expense(amount=1200.0, category="utilities", currency="INR", vendor="Electricity Board"),
        Expense(amount=799.0, category="subscription", currency="INR", vendor="Netflix"),
    ],
    "127": [
        Expense(amount=450.0, category="health", currency="INR", vendor="PharmEasy"),
    ]
}


@app.get("/", summary="Get all expenses")
def get_all_expenses() -> Dict[str, List[Expense]]:
    """Get all expenses for all users."""
    return EXPENSES_BY_USER

@app.get("/expenses/{user_id}", response_model=List[Expense], summary="Get user expenses")
def get_user_expenses(
    user_id: str = Path(..., description="User ID"),
    category: Optional[str] = Query(None, description="Filter by expense category")
) -> List[Expense]:
    """Get expenses for a specific user, optionally filtered by category."""
    if user_id not in EXPENSES_BY_USER:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_expenses = EXPENSES_BY_USER[user_id]
    
    if category is None:
        return user_expenses
    
    return [expense for expense in user_expenses 
            if expense.category.lower() == category.lower()]

@app.post("/expenses/{user_id}", response_model=Expense, status_code=201, summary="Add expense")
def add_expense(user_id: str, expense: Expense) -> Expense:
    """Add a new expense for a user."""
    if user_id not in EXPENSES_BY_USER:
        EXPENSES_BY_USER[user_id] = []
    
    EXPENSES_BY_USER[user_id].append(expense)
    return expense



