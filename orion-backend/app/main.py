"""
Main Application File

This file serves as the entry point for the Orion backend application.
It is responsible for:
- Creating and configuring the FastAPI application instance.
- Setting up middleware, such as CORS.
- Defining application startup and shutdown events.
- Including API routers from the different application modules.
- Defining global exception handlers and health check endpoints.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.modules.auth import routes as auth_routes
# Import other routers as they are created
# from app.modules.transactions import routes as transaction_routes
# from app.modules.ai import routes as ai_routes
# from app.modules.analytics import routes as analytics_routes

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- Application Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manages application startup and shutdown events.
    """
    logger.info("--- Starting up Orion Backend ---")
    # Note: In a production environment, database initialization and migrations
    # should be handled by Alembic, not here. This lifespan event is for
    # tasks like setting up connection pools or loading ML models.
    yield
    logger.info("--- Shutting down Orion Backend ---")


# --- FastAPI Application Instantiation ---
app = FastAPI(
    title="Orion - AI-Powered Financial Control Hub",
    description=(
        "This is the backend API for the Orion financial control hub. "
        "It provides endpoints for user authentication, financial data management, "
        "and AI-powered analytics."
    ),
    version="1.0.0",
    contact={
        "name": "Orion Development Team",
        "url": "https://github.com/yourusername/orion-ai-finance",
        "email": "contact@orion-finance.dev",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# --- Middleware Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard methods
    allow_headers=["*"],  # Allows all headers
)

# --- API Router Inclusion ---
# Include routers from different modules with a common prefix.
app.include_router(auth_routes.router, prefix="/api/v1")
# app.include_router(transaction_routes.router, prefix="/api/v1")
# app.include_router(ai_routes.router, prefix="/api/v1")
# app.include_router(analytics_routes.router, prefix="/api/v1")


# --- Root and Health Check Endpoints ---
@app.get("/", tags=["Monitoring"])
async def root():
    """Provides basic information about the API."""
    return {
        "message": "Welcome to the Orion Backend API",
        "version": app.version,
        "documentation": app.docs_url,
    }

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Returns a health status for monitoring purposes."""
    return {"status": "healthy"}


# --- Global Exception Handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Handles any uncaught exceptions in the application, preventing stack
    traces from being sent to the client.
    """
    logger.error(f"Unhandled exception for request {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )