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

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy import or_, and_, func, extract
from sqlalchemy.orm import Session, joinedload
import calendar
import uuid

from . import models, schemas
from ..auth.models import User
from ..audit.service import log_activity

# Constants
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 500

# Helper functions
def apply_transaction_filters(query, filters: schemas.TransactionFilters, user_id: int):
    """Apply filters to a transaction query"""
    query = query.filter(models.Transaction.user_id == user_id)
    
    if filters.start_date:
        query = query.filter(models.Transaction.date >= filters.start_date)
    if filters.end_date:
        # Include the entire end date
        end_date = datetime.combine(filters.end_date, datetime.max.time())
        query = query.filter(models.Transaction.date <= end_date)
    if filters.min_amount is not None:
        query = query.filter(models.Transaction.amount >= filters.min_amount)
    if filters.max_amount is not None:
        query = query.filter(models.Transaction.amount <= filters.max_amount)
    if filters.type:
        query = query.filter(models.Transaction.type == filters.type)
    if filters.category:
        query = query.filter(models.Transaction.category.ilike(f"%{filters.category}%"))
    if filters.account_id is not None:
        query = query.filter(models.Transaction.account_id == filters.account_id)
    if filters.payee_id is not None:
        query = query.filter(models.Transaction.payee_id == filters.payee_id)
    if filters.tags:
        for tag in filters.tags:
            query = query.filter(models.Transaction.tags.contains([tag]))
    if filters.search:
        search = f"%{filters.search}%"
        query = query.filter(
            or_(
                models.Transaction.description.ilike(search),
                models.Transaction.notes.ilike(search),
                models.Transaction.category.ilike(search),
                models.Transaction.subcategory.ilike(search)
            )
        )
    
    return query

# Transaction CRUD operations
def get_transaction(db: Session, transaction_id: int, user_id: int) -> Optional[models.Transaction]:
    """Get a single transaction by ID if it belongs to the user"""
    return db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == user_id
    ).first()

def get_transactions(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = DEFAULT_PAGE_SIZE,
    filters: Optional[schemas.TransactionFilters] = None
) -> Tuple[List[models.Transaction], int]:
    """
    Get transactions for a user with optional filtering and pagination.
    Returns a tuple of (transactions, total_count)
    """
    query = db.query(models.Transaction)
    
    # Apply filters if provided
    if filters:
        query = apply_transaction_filters(query, filters, user_id)
    else:
        query = query.filter(models.Transaction.user_id == user_id)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    limit = min(limit, MAX_PAGE_SIZE)  # Enforce max page size
    transactions = query.order_by(models.Transaction.date.desc())
    
    if skip:
        transactions = transactions.offset(skip)
    if limit:
        transactions = transactions.limit(limit)
    
    return transactions.all(), total

def create_transaction(
    db: Session, 
    transaction: schemas.TransactionCreate, 
    user_id: int,
    request: Optional[Any] = None
) -> models.Transaction:
    """Create a new transaction for a user"""
    db_transaction = models.Transaction(
        **transaction.model_dump(exclude_unset=True),
        user_id=user_id
    )
    
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Log the creation
    log_activity(
        db=db,
        action="transaction:create",
        user=db_transaction.owner,
        request=request,
        resource_type="transaction",
        resource_id=db_transaction.id,
        details={
            "amount": float(db_transaction.amount),
            "currency": db_transaction.currency,
            "type": db_transaction.type,
            "category": db_transaction.category
        }
    )
    
    return db_transaction

def update_transaction(
    db: Session, 
    transaction_id: int, 
    transaction_update: schemas.TransactionUpdate, 
    user_id: int,
    request: Optional[Any] = None
) -> Optional[models.Transaction]:
    """Update an existing transaction"""
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    
    update_data = transaction_update.model_dump(exclude_unset=True)
    
    # Store old values for audit log
    old_values = {
        "amount": float(db_transaction.amount),
        "category": db_transaction.category,
        "date": db_transaction.date.isoformat() if db_transaction.date else None
    }
    
    # Update fields
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db_transaction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_transaction)
    
    # Log the update
    log_activity(
        db=db,
        action="transaction:update",
        user_id=user_id,
        request=request,
        resource_type="transaction",
        resource_id=db_transaction.id,
        details={
            "old_values": old_values,
            "new_values": {
                "amount": float(db_transaction.amount),
                "category": db_transaction.category,
                "date": db_transaction.date.isoformat() if db_transaction.date else None
            }
        }
    )
    
    return db_transaction

def delete_transaction(
    db: Session, 
    transaction_id: int, 
    user_id: int,
    request: Optional[Any] = None
) -> bool:
    """Delete a transaction if it belongs to the user"""
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return False
    
    # Log before deletion
    log_activity(
        db=db,
        action="transaction:delete",
        user_id=user_id,
        request=request,
        resource_type="transaction",
        resource_id=transaction_id,
        details={
            "amount": float(db_transaction.amount),
            "currency": db_transaction.currency,
            "type": db_transaction.type,
            "category": db_transaction.category,
            "date": db_transaction.date.isoformat() if db_transaction.date else None
        }
    )
    
    db.delete(db_transaction)
    db.commit()
    return True

# Bulk operations
def bulk_update_transactions(
    db: Session,
    operation: schemas.BulkTransactionOperation,
    user_id: int,
    request: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Perform bulk operations on transactions (update, delete, categorize)
    Returns a summary of the operation
    """
    # Get the transactions that belong to the user
    transactions = db.query(models.Transaction).filter(
        models.Transaction.id.in_(operation.transaction_ids),
        models.Transaction.user_id == user_id
    ).all()
    
    if not transactions:
        return {"status": "error", "message": "No valid transactions found", "updated_count": 0}
    
    updated_count = 0
    
    if operation.operation == "update" and operation.updates:
        for transaction in transactions:
            for field, value in operation.updates.items():
                if hasattr(transaction, field):
                    setattr(transaction, field, value)
            transaction.updated_at = datetime.utcnow()
        updated_count = len(transactions)
        
    elif operation.operation == "delete":
        for transaction in transactions:
            db.delete(transaction)
        updated_count = len(transactions)
        
    elif operation.operation == "categorize" and operation.new_category:
        for transaction in transactions:
            transaction.category = operation.new_category
            transaction.updated_at = datetime.utcnow()
        updated_count = len(transactions)
    
    db.commit()
    
    # Log the bulk operation
    log_activity(
        db=db,
        action=f"transaction:bulk_{operation.operation}",
        user_id=user_id,
        request=request,
        resource_type="transaction",
        details={
            "operation": operation.operation,
            "transaction_count": updated_count,
            "updates": operation.updates if operation.operation == "update" else None,
            "new_category": operation.new_category if operation.operation == "categorize" else None
        }
    )
    
    return {
        "status": "success",
        "message": f"Successfully {operation.operation}d {updated_count} transactions",
        "updated_count": updated_count
    }

# Analytics and reporting
def get_transaction_stats(
    db: Session,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    group_by: str = "month"
) -> Dict[str, Any]:
    """
    Get transaction statistics for a user
    """
    # Default to current year if no date range provided
    if not start_date or not end_date:
        today = date.today()
        start_date = date(today.year, 1, 1)
        end_date = date(today.year, 12, 31)
    
    # Base query for transactions in date range
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.date.between(start_date, end_date)
    )
    
    # Get all transactions in the date range
    transactions = query.all()
    
    if not transactions:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "net_flow": 0,
            "by_category": {},
            "by_month": {}
        }
    
    # Calculate totals
    total_income = sum(
        t.amount for t in transactions 
        if t.type in [schemas.TransactionType.INCOME, schemas.TransactionType.INVESTMENT]
    )
    
    total_expenses = sum(
        abs(t.amount) for t in transactions 
        if t.type in [schemas.TransactionType.EXPENSE, schemas.TransactionType.TRANSFER]
    )
    
    # Group by category
    by_category = {}
    for t in transactions:
        if t.type in [schemas.TransactionType.EXPENSE, schemas.TransactionType.TRANSFER]:
            if t.category not in by_category:
                by_category[t.category] = 0
            by_category[t.category] += abs(t.amount)
    
    # Group by month
    by_month = {}
    current_date = start_date
    
    while current_date <= end_date:
        month_key = current_date.strftime("%Y-%m")
        month_transactions = [t for t in transactions 
                           if t.date and t.date.month == current_date.month and t.date.year == current_date.year]
        
        month_income = sum(t.amount for t in month_transactions 
                          if t.type in [schemas.TransactionType.INCOME, schemas.TransactionType.INVESTMENT])
        
        month_expenses = sum(abs(t.amount) for t in month_transactions 
                            if t.type in [schemas.TransactionType.EXPENSE, schemas.TransactionType.TRANSFER])
        
        by_month[month_key] = {
            "income": month_income,
            "expenses": month_expenses,
            "net": month_income - month_expenses
        }
        
        # Move to first day of next month
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_flow": total_income - total_expenses,
        "by_category": by_category,
        "by_month": by_month
    }

def get_category_insights(
    db: Session,
    user_id: int,
    category: str,
    months: int = 12
) -> Dict[str, Any]:
    """
    Get insights for a specific category over the last N months
    """
    end_date = date.today()
    start_date = date(end_date.year, end_date.month, 1) - timedelta(days=30 * (months - 1))
    
    # Get transactions in this category
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.category == category,
        models.Transaction.date.between(start_date, end_date)
    ).order_by(models.Transaction.date).all()
    
    if not transactions:
        return {
            "category": category,
            "total_amount": 0,
            "transaction_count": 0,
            "monthly_average": 0,
            "monthly_breakdown": {},
            "largest_transaction": None,
            "recent_transactions": []
        }
    
    # Calculate statistics
    total_amount = sum(abs(t.amount) for t in transactions)
    monthly_average = total_amount / months
    
    # Monthly breakdown
    monthly_breakdown = {}
    current_date = start_date
    
    while current_date <= end_date:
        month_key = current_date.strftime("%Y-%m")
        month_transactions = [t for t in transactions 
                           if t.date and t.date.month == current_date.month and t.date.year == current_date.year]
        
        monthly_breakdown[month_key] = {
            "amount": sum(abs(t.amount) for t in month_transactions),
            "transaction_count": len(month_transactions)
        }
        
        # Move to next month
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)
    
    # Find largest transaction
    largest_transaction = max(transactions, key=lambda t: abs(t.amount))
    
    # Get recent transactions (last 5)
    recent_transactions = sorted(transactions, key=lambda t: t.date or date.min, reverse=True)[:5]
    
    return {
        "category": category,
        "total_amount": total_amount,
        "transaction_count": len(transactions),
        "monthly_average": monthly_average,
        "monthly_breakdown": monthly_breakdown,
        "largest_transaction": {
            "id": largest_transaction.id,
            "amount": float(largest_transaction.amount),
            "date": largest_transaction.date.isoformat() if largest_transaction.date else None,
            "description": largest_transaction.description
        },
        "recent_transactions": [
            {
                "id": t.id,
                "amount": float(t.amount),
                "date": t.date.isoformat() if t.date else None,
                "description": t.description
            }
            for t in recent_transactions
        ]
    }