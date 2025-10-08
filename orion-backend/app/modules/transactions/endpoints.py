from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from . import schemas, service, models
from ..auth.models import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """
    Create a new transaction
    """
    return service.create_transaction(db, transaction, current_user.id, request)

@router.get("/", response_model=schemas.TransactionResponse)
async def list_transactions(
    skip: int = 0,
    limit: int = 50,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    type: Optional[schemas.TransactionType] = None,
    category: Optional[str] = None,
    account_id: Optional[int] = None,
    payee_id: Optional[int] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all transactions with optional filtering
    """
    tag_list = tags.split(",") if tags else None
    
    filters = schemas.TransactionFilters(
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        type=type,
        category=category,
        account_id=account_id,
        payee_id=payee_id,
        tags=tag_list,
        search=search
    )
    
    transactions, total = service.get_transactions(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        filters=filters
    )
    
    return {
        "items": transactions,
        "total": total,
        "page": (skip // limit) + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
async def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific transaction by ID
    """
    transaction = service.get_transaction(db, transaction_id, current_user.id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.put("/{transaction_id}", response_model=schemas.TransactionRead)
async def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """
    Update an existing transaction
    """
    transaction = service.update_transaction(
        db=db,
        transaction_id=transaction_id,
        transaction_update=transaction_update,
        user_id=current_user.id,
        request=request
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """
    Delete a transaction
    """
    success = service.delete_transaction(
        db=db,
        transaction_id=transaction_id,
        user_id=current_user.id,
        request=request
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return None

@router.post("/bulk", response_model=dict)
async def bulk_operation(
    operation: schemas.BulkTransactionOperation,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    request: Request = None
):
    """
    Perform bulk operations on transactions (update, delete, categorize)
    """
    return service.bulk_update_transactions(
        db=db,
        operation=operation,
        user_id=current_user.id,
        request=request
    )

@router.get("/stats/summary", response_model=schemas.TransactionStats)
async def get_transaction_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    group_by: str = "month",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get transaction statistics and summary
    """
    return service.get_transaction_stats(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        group_by=group_by
    )

@router.get("/category/{category}/insights", response_model=dict)
async def get_category_insights(
    category: str,
    months: int = 12,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get insights for a specific transaction category
    """
    return service.get_category_insights(
        db=db,
        user_id=current_user.id,
        category=category,
        months=months
    )

@router.get("/export", response_model=List[schemas.TransactionRead])
async def export_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    format: str = "json",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Export transactions in the specified format (JSON or CSV)
    """
    filters = schemas.TransactionFilters(
        start_date=start_date,
        end_date=end_date
    )
    
    transactions, _ = service.get_transactions(
        db=db,
        user_id=current_user.id,
        filters=filters
    )
    
    # In a real implementation, you would format the response based on the requested format
    # For now, we'll just return the JSON response
    return transactions
