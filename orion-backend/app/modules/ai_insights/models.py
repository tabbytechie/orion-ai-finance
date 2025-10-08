from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.database import Base

class InsightType(str, Enum):
    SPENDING_PATTERN = "spending_pattern"
    INCOME_ANALYSIS = "income_analysis"
    BUDGET_ALERT = "budget_alert"
    SAVINGS_OPPORTUNITY = "savings_opportunity"
    FINANCIAL_HEALTH = "financial_health"
    ANOMALY_DETECTION = "anomaly_detection"
    CATEGORIZATION = "categorization"

class InsightSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class InsightStatus(str, Enum):
    ACTIVE = "active"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"

class AIIntent(str, Enum):
    ANALYZE_SPENDING = "analyze_spending"
    PREDICT_FUTURE = "predict_future"
    DETECT_ANOMALIES = "detect_anomalies"
    SUGGEST_BUDGET = "suggest_budget"
    OPTIMIZE_SAVINGS = "optimize_savings"
    CATEGORIZE_TRANSACTIONS = "categorize_transactions"

class FinancialInsight(Base):
    """Model for storing AI-generated financial insights"""
    __tablename__ = "financial_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Insight metadata
    type = Column(SQLEnum(InsightType), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    severity = Column(SQLEnum(InsightSeverity), default=InsightSeverity.INFO)
    status = Column(SQLEnum(InsightStatus), default=InsightStatus.ACTIVE)
    
    # AI-specific fields
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    metadata_ = Column("metadata", JSON, default={})  # Additional metadata in JSON format
    
    # Related transactions or categories (stored as JSON for flexibility)
    related_entities = Column(JSON, default=[])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="financial_insights")

class AITrainingJob(Base):
    """Model for tracking AI model training jobs"""
    __tablename__ = "ai_training_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Job metadata
    intent = Column(SQLEnum(AIIntent), nullable=False)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Input/output data
    input_parameters = Column(JSON, default={})
    result = Column(JSON, nullable=True)
    error = Column(String(1000), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ai_training_jobs")

# Pydantic models for request/response
class InsightBase(BaseModel):
    type: InsightType
    title: str
    description: Optional[str] = None
    severity: InsightSeverity = InsightSeverity.INFO
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Dict[str, Any] = {}
    related_entities: List[Dict[str, Any]] = []

class InsightCreate(InsightBase):
    pass

class InsightUpdate(BaseModel):
    status: Optional[InsightStatus] = None

class InsightResponse(InsightBase):
    id: int
    user_id: int
    status: InsightStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class AITrainingJobCreate(BaseModel):
    intent: AIIntent
    parameters: Dict[str, Any] = {}

class AITrainingJobResponse(BaseModel):
    id: int
    user_id: int
    intent: AIIntent
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
