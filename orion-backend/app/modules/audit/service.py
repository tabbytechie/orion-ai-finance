from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import Request
import json

from . import models, schemas
from ..auth.models import User

def create_audit_log(
    db: Session,
    action: str,
    status: str = "success",
    user_id: Optional[int] = None,
    request: Optional[Request] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None,
) -> models.AuditLog:
    """
    Create a new audit log entry
    """
    ip_address = None
    user_agent = None
    
    if request:
        # Get client IP address
        if "x-forwarded-for" in request.headers:
            ip_address = request.headers["x-forwarded-for"].split(",")[0]
        else:
            ip_address = request.client.host if request.client else None
        
        # Get user agent
        user_agent = request.headers.get("user-agent")
    
    # Create the audit log
    db_audit_log = models.AuditLog(
        user_id=user_id,
        action=action,
        status=status,
        ip_address=ip_address,
        user_agent=user_agent,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id is not None else None,
        details=details or {},
        error_message=error_message,
    )
    
    db.add(db_audit_log)
    db.commit()
    db.refresh(db_audit_log)
    
    return db_audit_log

def get_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    status: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> tuple[List[models.AuditLog], int]:
    """
    Retrieve audit logs with filtering and pagination
    """
    query = db.query(models.AuditLog)
    
    # Apply filters
    if user_id is not None:
        query = query.filter(models.AuditLog.user_id == user_id)
    if action:
        query = query.filter(models.AuditLog.action == action)
    if status:
        query = query.filter(models.AuditLog.status == status)
    if resource_type:
        query = query.filter(models.AuditLog.resource_type == resource_type)
    if resource_id is not None:
        query = query.filter(models.AuditLog.resource_id == str(resource_id))
    if start_date:
        query = query.filter(models.AuditLog.created_at >= start_date)
    if end_date:
        # Include the entire end date
        end_of_day = datetime(
            year=end_date.year,
            month=end_date.month,
            day=end_date.day,
            hour=23,
            minute=59,
            second=59
        )
        query = query.filter(models.AuditLog.created_at <= end_of_day)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    query = query.order_by(models.AuditLog.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    return query.all(), total

def log_activity(
    db: Session,
    action: str,
    user: Optional[User] = None,
    request: Optional[Request] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    status: str = "success",
    error_message: Optional[str] = None,
) -> models.AuditLog:
    """
    Helper function to log user activity
    """
    return create_audit_log(
        db=db,
        action=action,
        status=status,
        user_id=user.id if user else None,
        request=request,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        error_message=error_message,
    )
