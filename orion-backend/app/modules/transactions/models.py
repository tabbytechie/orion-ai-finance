"""
SQLAlchemy Models for the Transactions Module

This file defines the database models related to financial transactions.
"""

import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class TransactionType(str, enum.Enum):
    """Enumeration for the type of transaction."""
    INCOME = "income"
    EXPENSE = "expense"

class Transaction(Base):
    """
    Represents a single financial transaction in the system.

    This model stores all the details about an income or expense event,
    linking it to a specific user.
    """
    __tablename__ = "transactions"

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the transaction.")
    description = Column(String, index=True, nullable=False, doc="A brief description of the transaction.")
    amount = Column(Float, nullable=False, doc="The monetary value of the transaction.")
    category = Column(String, index=True, nullable=False, doc="The category of the transaction (e.g., 'Groceries', 'Salary').")
    type = Column(
        Enum(TransactionType),
        nullable=False,
        default=TransactionType.EXPENSE,
        doc="The type of transaction, either 'income' or 'expense'."
    )
    date = Column(DateTime(timezone=True), nullable=False, doc="The date and time when the transaction occurred.")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, doc="The ID of the user who owns this transaction.")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when the transaction was created."
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp of the last update to the transaction record."
    )

    # --- Relationships ---
    # Defines the many-to-one relationship from Transaction to User.
    owner = relationship("User", back_populates="transactions")