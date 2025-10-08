from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from app.core.config import settings
from app.core.database import engine, Base, init_db
from app.modules.auth import routes as auth_routes
from app.modules.transactions import routes as transaction_routes
from app.modules.ai import routes as ai_routes
from app.modules.analytics import routes as analytics_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handle application startup and shutdown events.
    """
    try:
        # Initialize database tables only if not in testing mode
        if not settings.TESTING:
            logger.info("Initializing database...")
            init_db()
            logger.info("Database initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Error during application startup: {str(e)}")
        raise

# Create FastAPI application
app = FastAPI(
    title="Orion - AI-Powered Financial Control Hub",
    description="The backend for the Orion financial control hub.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Range"],
    max_age=600,
)

# Include module routers
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(transaction_routes.router, prefix="/api/v1")
app.include_router(ai_routes.router, prefix="/api/v1")
app.include_router(analytics_routes.router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "message": "Orion API is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Orion Backend API",
        "docs": "/docs",
        "version": "0.1.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for uncaught exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )