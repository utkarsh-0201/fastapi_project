"""FastAPI Expense Tracker API - Main Application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.lifespan import lifespan

# Import all models to ensure they're registered with SQLModel
from app.models import currency, expense, user  # noqa: F401
from app.routers import auth, currencies, expenses

# Setup logging
setup_logging()

# Load settings
settings = get_settings()

# Create FastAPI app with lifespan for DB initialization
app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="A simple expense tracking API with CRUD operations",
    lifespan=lifespan,
)

# Middleware: GZip for responses and CORS using configured origins
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(expenses.router)
app.include_router(currencies.router)
app.include_router(auth.router)
