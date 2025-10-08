from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from ..auth.schemas import UserResponse

class AuditLogBase(BaseModel):
    action: str
    status: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: int
    user: Optional[UserResponse] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogFilter(BaseModel):
    user_id: Optional[int] = None
    action: Optional[str] = None
    status: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "action": "login",
                "status": "success",
                "resource_type": "user",
                "start_date": "2023-01-01T00:00:00",
                "end_date": "2023-12-31T23:59:59"
            }
        }

class AuditLogsResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
