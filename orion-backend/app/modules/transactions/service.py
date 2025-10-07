from sqlalchemy.orm import Session
from . import models, schemas

def get_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Fetches all transactions for a specific user with pagination.
    """
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).offset(skip).limit(limit).all()

def create_user_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    """
    Creates a new transaction for a specific user.
    """
    db_transaction = models.Transaction(
        **transaction.model_dump(),
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction