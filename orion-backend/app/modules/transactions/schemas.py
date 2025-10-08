"""
Pydantic Schemas for the Transactions Module

This file defines the Pydantic models used for data validation, serialization,
and documentation in the transaction-related API endpoints.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .models import TransactionType

# --- Base and Creation Schemas ---

class TransactionBase(BaseModel):
    """Base schema for transaction properties."""
    description: str = Field(..., description="A description of the transaction.", example="Monthly salary")
    amount: float = Field(..., gt=0, description="The transaction amount, must be positive.", example=5000.00)
    category: str = Field(..., description="The category of the transaction.", example="Salary")
    type: TransactionType = Field(..., description="The type of transaction.", example=TransactionType.INCOME)
    date: datetime = Field(..., description="The date of the transaction.", example=datetime.now())

class TransactionCreate(TransactionBase):
    """Schema used for creating a new transaction."""
    pass

class TransactionUpdate(BaseModel):
    """
    Schema for updating an existing transaction.
    All fields are optional to allow for partial updates.
    """
    description: Optional[str] = Field(None, description="A new description for the transaction.")
    amount: Optional[float] = Field(None, gt=0, description="A new amount for the transaction.")
    category: Optional[str] = Field(None, description="A new category for the transaction.")
    type: Optional[TransactionType] = Field(None, description="A new type for the transaction.")
    date: Optional[datetime] = Field(None, description="A new date for the transaction.")

# --- Public Response Schema ---

class TransactionPublic(TransactionBase):
    """
    Schema for representing a transaction in API responses.
    This includes read-only fields like ID and timestamps.
    """
    id: int = Field(..., description="Unique identifier for the transaction.", example=1)
    user_id: int = Field(..., description="The ID of the user who owns the transaction.", example=1)
    created_at: datetime = Field(..., description="Timestamp when the transaction was created.")
    updated_at: datetime = Field(..., description="Timestamp of the last update.")

    class Config:
        from_attributes = True