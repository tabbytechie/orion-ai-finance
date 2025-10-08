"""
Service Layer for the Transactions Module

This module contains the business logic for managing financial transactions.
It provides an abstraction layer between the API routes and the database models,
handling all data operations related to transactions.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

# --- Read Operations ---

def get_transaction(db: Session, transaction_id: int) -> Optional[models.Transaction]:
    """
    Fetches a single transaction by its ID.

    Args:
        db (Session): The database session.
        transaction_id (int): The ID of the transaction to fetch.

    Returns:
        Optional[models.Transaction]: The transaction object if found, otherwise None.
    """
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def get_transactions_by_user(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[models.Transaction]:
    """
    Fetches a paginated list of transactions for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user whose transactions to fetch.
        skip (int): The number of records to skip for pagination.
        limit (int): The maximum number of records to return.

    Returns:
        List[models.Transaction]: A list of transaction objects.
    """
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# --- Write Operations ---

def create_user_transaction(
    db: Session, transaction: schemas.TransactionCreate, user_id: int
) -> models.Transaction:
    """
    Creates a new transaction for a specific user.

    Args:
        db (Session): The database session.
        transaction (schemas.TransactionCreate): The transaction creation data.
        user_id (int): The ID of the user creating the transaction.

    Returns:
        models.Transaction: The newly created transaction object.
    """
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=user_id)
    db.add(db_transaction)
    db.flush()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(
    db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate, user_id: int
) -> Optional[models.Transaction]:
    """
    Updates an existing transaction.

    Ensures that a user can only update their own transactions.

    Args:
        db (Session): The database session.
        transaction_id (int): The ID of the transaction to update.
        transaction_update (schemas.TransactionUpdate): The data to update.
        user_id (int): The ID of the user requesting the update.

    Returns:
        Optional[models.Transaction]: The updated transaction object, or None if not found
                                     or not owned by the user.
    """
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction or db_transaction.user_id != user_id:
        return None  # Transaction not found or not owned by user

    update_data = transaction_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.add(db_transaction)
    db.flush()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    """
    Deletes a transaction.

    Ensures that a user can only delete their own transactions.

    Args:
        db (Session): The database session.
        transaction_id (int): The ID of the transaction to delete.
        user_id (int): The ID of the user requesting the deletion.

    Returns:
        bool: True if the transaction was deleted, False otherwise.
    """
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction or db_transaction.user_id != user_id:
        return False  # Transaction not found or not owned by user

    db.delete(db_transaction)
    db.flush()
    return True