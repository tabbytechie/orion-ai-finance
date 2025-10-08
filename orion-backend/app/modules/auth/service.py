"""
Service Layer for the Auth Module

This module contains the business logic for user authentication and management.
It is responsible for interacting with the database and performing operations
related to the User model. The service layer is designed to be called by the
API routes, separating business logic from the HTTP layer.
"""

from sqlalchemy.orm import Session
from typing import Optional
from app.core.security import get_password_hash, verify_password
from . import models, schemas

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Fetches a user by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to fetch.

    Returns:
        Optional[models.User]: The user object if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Creates a new user in the database.

    This function hashes the user's password and creates a new User record.
    It does NOT commit the transaction; the calling function is responsible
    for session management (commit, rollback, etc.).

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user creation data.

    Returns:
        models.User: The newly created user object.

    Raises:
        ValueError: If a user with the same email already exists.
    """
    if get_user_by_email(db, user.email):
        raise ValueError("A user with this email address already exists.")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.flush()  # Use flush to assign an ID to db_user without committing
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """
    Authenticates a user by checking their email and password.

    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's plain-text password.

    Returns:
        Optional[models.User]: The authenticated user object if credentials
                               are valid, otherwise None.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None  # User not found

    if not verify_password(password, user.hashed_password):
        return None  # Invalid password

    return user