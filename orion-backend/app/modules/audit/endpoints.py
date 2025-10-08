from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user, get_current_active_admin_user
from . import schemas, service, models
from ..auth.models import User

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("/logs", response_model=schemas.AuditLogsResponse)
async def get_audit_logs(
    skip: int = 0,
    limit: int = 50,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    status: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)  # Only admins can access audit logs
):
    """
    Get audit logs with filtering and pagination
    """
    # Regular users can only see their own audit logs
    if not current_user.is_admin and user_id != current_user.id:
        user_id = current_user.id
    
    logs, total = service.get_audit_logs(
        db=db,
        skip=skip,
        limit=min(limit, 200),  # Enforce max limit
        user_id=user_id,
        action=action,
        status=status,
        resource_type=resource_type,
        resource_id=resource_id,
        start_date=start_date,
        end_date=end_date,
        search=search
    )
    
    return {
        "items": logs,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
    }

@router.get("/logs/{log_id}", response_model=schemas.AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)  # Only admins can access audit logs
):
    """
    Get a specific audit log by ID
    """
    log = db.query(models.AuditLog).filter(models.AuditLog.id == log_id).first()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log not found"
        )
    
    # Regular users can only see their own audit logs
    if not current_user.is_admin and log.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this audit log"
        )
    
    return log

@router.get("/user-activity", response_model=List[schemas.AuditLogResponse])
async def get_user_activity(
    days: int = 30,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get recent activity for the current user
    """
    end_date = datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=days)
    
    query = db.query(models.AuditLog).filter(
        models.AuditLog.user_id == current_user.id,
        models.AuditLog.created_at >= start_date,
        models.AuditLog.created_at <= end_date
    )
    
    if action:
        query = query.filter(models.AuditLog.action == action)
    
    return query.order_by(models.AuditLog.created_at.desc()).limit(100).all()

@router.get("/system-activity", response_model=List[schemas.AuditLogResponse])
async def get_system_activity(
    days: int = 7,
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)  # Only admins can access system activity
):
    """
    Get recent system activity (admin only)
    """
    end_date = datetime.utcnow()
    start_date = end_date - datetime.timedelta(days=days)
    
    query = db.query(models.AuditLog).filter(
        models.AuditLog.created_at >= start_date,
        models.AuditLog.created_at <= end_date
    )
    
    if action:
        query = query.filter(models.AuditLog.action == action)
    
    return query.order_by(models.AuditLog.created_at.desc()).limit(1000).all()

@router.get("/export", response_model=List[schemas.AuditLogResponse])
async def export_audit_logs(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    format: str = "json",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)  # Only admins can export audit logs
):
    """
    Export audit logs in the specified format (JSON or CSV)
    """
    query = db.query(models.AuditLog)
    
    if start_date:
        query = query.filter(models.AuditLog.created_at >= start_date)
    if end_date:
        # Include the entire end date
        end_datetime = datetime.combine(end_date, datetime.max.time())
        query = query.filter(models.AuditLog.created_at <= end_datetime)
    
    logs = query.order_by(models.AuditLog.created_at.desc()).limit(10000).all()
    
    # In a real implementation, you would format the response based on the requested format
    # For now, we'll just return the JSON response
    return logs
