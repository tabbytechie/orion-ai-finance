"""
API Routes for Authentication

This module defines the API endpoints related to user authentication, including
user registration, login (token issuance), and retrieving user information.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.dependencies import get_current_user
from . import schemas, service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=schemas.UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with a unique email address."
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Handles the user registration process.
    - Validates input data.
    - Checks for existing users.
    - Creates the user if validation passes.
    """
    try:
        new_user = service.create_user(db=db, user=user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during user registration.",
        )

@router.post(
    "/login",
    response_model=schemas.Token,
    summary="User login",
    description="Authenticate a user with an email and password to obtain a JWT access token."
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Handles user authentication.
    - Verifies credentials.
    - Issues a JWT if credentials are valid.
    """
    user = service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=schemas.UserPublic,
    summary="Get current user",
    description="Retrieve the details of the currently authenticated user."
)
def read_users_me(current_user: schemas.UserPublic = Depends(get_current_user)):
    """
    Provides a secure endpoint to fetch the current user's data.
    The `get_current_user` dependency handles token validation.
    """
    return current_user