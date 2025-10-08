from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base

class AuditActionType(str, Enum):
    """Types of actions that can be audited"""
    LOGIN = "login"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    PERMISSION_CHANGE = "permission_change"
    ROLE_CHANGE = "role_change"
    SETTINGS_UPDATE = "settings_update"
    SYSTEM = "system"
    OTHER = "other"

class AuditStatus(str, Enum):
    """Status of the audited action"""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"

class AuditLog(Base):
    """Audit log model for tracking user actions and system events"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Action details
    action = Column(SQLEnum(AuditActionType), nullable=False)
    status = Column(SQLEnum(AuditStatus), default=AuditStatus.SUCCESS, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 addresses can be up to 45 chars
    user_agent = Column(Text, nullable=True)
    
    # Resource details
    resource_type = Column(String(100), nullable=True)  # e.g., 'user', 'transaction', 'account'
    resource_id = Column(String(100), nullable=True)    # ID of the affected resource
    
    # Additional context
    details = Column(JSON, default=dict, nullable=True)  # Additional context about the action
    error_message = Column(Text, nullable=True)          # Error message if status is FAILURE
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.id} {self.action} {self.status}>"
