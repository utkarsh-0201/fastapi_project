"""FastAPI Expense Tracker API - Main Application."""
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.db.lifespan import lifespan

# Import all models to ensure they're registered with SQLModel
from app.models import currency, expense, user  # noqa: F401
from app.routers import currencies, expenses

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="A simple expense tracking API with CRUD operations",
    lifespan=lifespan,
)

# Include routers
app.include_router(expenses.router)
app.include_router(currencies.router)
