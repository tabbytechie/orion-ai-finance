from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.modules.auth import models as auth_models
from . import schemas, service

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    """
    Create a new transaction for the current user.
    """
    return service.create_user_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/", response_model=List[schemas.TransactionRead])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_user)
):
    """
    Retrieve all transactions for the current user.
    """
    transactions = service.get_transactions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions