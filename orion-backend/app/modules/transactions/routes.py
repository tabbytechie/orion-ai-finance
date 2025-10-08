"""
API Routes for Transactions

This module defines the API endpoints for creating, reading, updating, and
deleting financial transactions. All endpoints in this module require user
authentication.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.modules.auth import models as auth_models
from . import schemas, service

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    dependencies=[Depends(get_current_user)],
)

@router.post(
    "/",
    response_model=schemas.TransactionPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transaction",
)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user),
):
    """
    Creates a new transaction record for the currently authenticated user.
    """
    try:
        new_transaction = service.create_user_transaction(
            db=db, transaction=transaction, user_id=current_user.id
        )
        db.commit()
        db.refresh(new_transaction)
        return new_transaction
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create transaction.",
        )

@router.get(
    "/",
    response_model=List[schemas.TransactionPublic],
    summary="List all transactions for the current user",
)
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user),
):
    """
    Retrieves a paginated list of all transactions recorded by the current user.
    """
    transactions = service.get_transactions_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return transactions

@router.get(
    "/{transaction_id}",
    response_model=schemas.TransactionPublic,
    summary="Get a single transaction by ID",
)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user),
):
    """
    Retrieves the details of a specific transaction by its ID.
    A user can only retrieve their own transactions.
    """
    db_transaction = service.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None or db_transaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return db_transaction

@router.put(
    "/{transaction_id}",
    response_model=schemas.TransactionPublic,
    summary="Update a transaction",
)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user),
):
    """
    Updates the details of a specific transaction.
    A user can only update their own transactions.
    """
    updated_transaction = service.update_transaction(
        db,
        transaction_id=transaction_id,
        transaction_update=transaction,
        user_id=current_user.id,
    )
    if updated_transaction is None:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    db.commit()
    return updated_transaction

@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a transaction",
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user),
):
    """
    Deletes a specific transaction by its ID.
    A user can only delete their own transactions.
    """
    success = service.delete_transaction(
        db, transaction_id=transaction_id, user_id=current_user.id
    )
    if not success:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    db.commit()
    return None