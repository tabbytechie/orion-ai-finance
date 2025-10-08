"""
Pydantic Schemas for the Auth Module

This file defines the Pydantic models used for data validation, serialization,
and documentation in the authentication-related API endpoints. These schemas
ensure that data conforms to the expected structure for requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from .models import UserRole

# --- Token Schemas ---

class Token(BaseModel):
    """Schema for the JWT access token response."""
    access_token: str = Field(
        ...,
        description="The JWT access token.",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        "bearer",
        description="The type of the token.",
        example="bearer"
    )

class TokenData(BaseModel):
    """Schema for the data encoded within the JWT."""
    email: EmailStr = Field(..., description="The user's email address (subject of the token).")

# --- User Schemas ---

class UserBase(BaseModel):
    """Base schema for user properties, containing shared attributes."""
    email: EmailStr = Field(..., description="The user's email address.", example="user@example.com")
    role: UserRole = Field(UserRole.user, description="The role assigned to the user.", example="user")

class UserCreate(UserBase):
    """Schema for creating a new user. Includes the password."""
    password: str = Field(..., min_length=8, description="The user's password (min 8 characters).", example="a_strong_password")

class UserRead(UserBase):
    """
    Schema for reading user data from the database.

    This schema is used for internal representation and includes all user fields,
    including the user's ID. It's configured to work with ORM models.
    """
    id: int = Field(..., description="The unique identifier for the user.", example=1)

    class Config:
        from_attributes = True

class UserPublic(UserBase):
    """
    Schema for publicly exposed user information.

    This schema is used in API responses to avoid exposing sensitive or
    internal data. It includes the user's ID and timestamps.
    """
    id: int = Field(..., description="The unique identifier for the user.", example=1)
    created_at: datetime = Field(..., description="The timestamp when the user was created.")
    updated_at: datetime = Field(..., description="The timestamp of the last update.")

    class Config:
        from_attributes = True