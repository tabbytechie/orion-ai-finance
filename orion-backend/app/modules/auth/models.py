"""
SQLAlchemy Models for the Auth Module

This file defines the database models related to user authentication,
including the User model and associated enumerations.
"""

import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str, enum.Enum):
    """Enumeration for user roles within the system."""
    admin = "admin"          # Full administrative access
    user = "user"            # Standard user access
    accountant = "accountant"  # Access to financial data, but no admin rights

class User(Base):
    """
    Represents a user in the system.

    This model stores essential user information, including credentials and role.
    """
    __tablename__ = "users"

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True, doc="Unique identifier for the user.")
    email = Column(String, unique=True, index=True, nullable=False, doc="User's email address, used for login.")
    hashed_password = Column(String, nullable=False, doc="Hashed password for the user.")
    role = Column(
        Enum(UserRole),
        default=UserRole.user,
        nullable=False,
        doc="The role assigned to the user, determining their permissions."
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when the user was created."
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp of the last update to the user's record."
    )

    # --- Relationships ---
    # Defines the one-to-many relationship between a user and their transactions.
    transactions = relationship("Transaction", back_populates="owner")