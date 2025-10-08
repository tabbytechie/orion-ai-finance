"""
Database Connection and Session Management

This module is responsible for setting up the database connection and providing
a session management mechanism for the FastAPI application.

Key Components:
- `engine`: The core SQLAlchemy engine, configured with connection pooling
  for efficient database communication in a production environment.
- `SessionLocal`: A sessionmaker class that creates new database sessions.
- `Base`: The declarative base for SQLAlchemy models. All models in the
  application should inherit from this class.
- `get_db`: A FastAPI dependency that provides a database session for each
  incoming request and ensures it is properly closed afterward.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from .config import settings

# --- SQLAlchemy Engine Setup ---
# The engine is configured with settings optimized for a production server,
# including connection pooling and liveness checks.
engine = create_engine(
    str(settings.DATABASE_URL),  # Use str() to ensure Pydantic DSN is converted
    pool_pre_ping=True,          # Checks for "live" connections before use
    pool_size=10,                # Max number of connections to keep in the pool
    max_overflow=20,             # Max connections to allow beyond pool_size
    pool_recycle=1800,           # Recycle connections after 30 minutes
    pool_timeout=30,             # Time to wait for a connection from the pool
)

# --- Session Factory ---
# SessionLocal is a factory for creating new Session objects. It's configured
# to not autocommit or autoflush, giving us fine-grained control over
# transaction lifecycles.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Declarative Base ---
# All SQLAlchemy ORM models will inherit from this Base class.
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to get a database session per request.

    This function yields a new database session for each request and ensures
    that the session is always closed when the request is finished, even if
    an error occurs.

    Note: This dependency does NOT commit the session. Transaction commits
    should be handled explicitly within the business logic (service layer)
    to ensure data integrity and clear control over transactions.

    Yields:
        Generator[Session, None, None]: A SQLAlchemy Session object.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initializes the database by creating all tables.

    Note: This function is intended for initial setup or testing environments.
    In production, database schema migrations should be managed by Alembic.
    """
    Base.metadata.create_all(bind=engine)