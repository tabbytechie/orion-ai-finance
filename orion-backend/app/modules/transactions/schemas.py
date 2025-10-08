import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from pydantic import BaseModel, Field, field_validator, model_validator
from ..auth.schemas import UserResponse

# Enums for schema validation
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
    SAVINGS = "savings"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RECURRING = "recurring"

class RecurringFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

# Base schema for Transaction properties
class TransactionBase(BaseModel):
    description: Optional[str] = Field(
        None, 
        description="A brief description of the transaction",
        max_length=255
    )
    amount: float = Field(..., gt=0, description="The amount of the transaction (must be positive)")
    currency: str = Field("USD", min_length=3, max_length=3, description="ISO 4217 currency code")
    type: TransactionType = Field(..., description="The type of transaction")
    status: TransactionStatus = Field(default=TransactionStatus.COMPLETED, description="Current status of the transaction")
    category: str = Field(..., max_length=50, description="Main category of the transaction")
    subcategory: Optional[str] = Field(None, max_length=50, description="Optional subcategory for more specific classification")
    date: datetime.date = Field(default_factory=datetime.date.today, description="The date when the transaction occurred")
    is_recurring: bool = Field(False, description="Whether this is a recurring transaction")
    recurring_id: Optional[str] = Field(None, description="ID to group recurring transactions")
    frequency: Optional[RecurringFrequency] = Field(None, description="Frequency of recurring transactions")
    end_date: Optional[datetime.date] = Field(None, description="End date for recurring transactions")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes about the transaction")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for categorizing transactions")
    attachments: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list, 
        description="List of file attachments (references or metadata)"
    )
    account_id: Optional[int] = Field(None, description="ID of the associated account")
    payee_id: Optional[int] = Field(None, description="ID of the payee")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Additional metadata for the transaction"
    )

    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(v, 2)  # Ensure 2 decimal places for currency

    @model_validator(mode='after')
    def validate_recurring_fields(self):
        if self.is_recurring and not self.recurring_id:
            self.recurring_id = f"rec_{self.date.strftime('%Y%m%d')}_{id(self)}"
        
        if self.is_recurring and not self.frequency:
            raise ValueError("Frequency is required for recurring transactions")
            
        if self.frequency and not self.is_recurring:
            self.is_recurring = True
            
        return self

# Schema for creating a new transaction
class TransactionCreate(TransactionBase):
    pass

# Schema for updating a transaction
class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    type: Optional[TransactionType] = None
    status: Optional[TransactionStatus] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    date: Optional[datetime.date] = None
    is_recurring: Optional[bool] = None
    frequency: Optional[RecurringFrequency] = None
    end_date: Optional[datetime.date] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    account_id: Optional[int] = None
    payee_id: Optional[int] = None
    
    @model_validator(mode='after')
    def validate_update(self):
        if self.amount is not None and self.amount <= 0:
            raise ValueError('Amount must be greater than 0')
        return self

# Schema for reading transaction data
class TransactionRead(TransactionBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        from_attributes = True

# Schema for transaction filters
class TransactionFilters(BaseModel):
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    account_id: Optional[int] = None
    payee_id: Optional[int] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "min_amount": 10.0,
                "max_amount": 1000.0,
                "type": "expense",
                "category": "groceries",
                "tags": ["food", "monthly"]
            }
        }

# Schema for bulk transaction operations
class BulkTransactionOperation(BaseModel):
    operation: Literal["update", "delete", "categorize"]
    transaction_ids: List[int]
    updates: Optional[Dict[str, Any]] = None
    new_category: Optional[str] = None
    
    @model_validator(mode='after')
    def validate_operation(self):
        if self.operation == "update" and not self.updates:
            raise ValueError("Updates must be provided for 'update' operation")
        if self.operation == "categorize" and not self.new_category:
            raise ValueError("new_category must be provided for 'categorize' operation")
        return self

# Schema for transaction statistics
class TransactionStats(BaseModel):
    total_income: float
    total_expenses: float
    net_flow: float
    by_category: Dict[str, float]
    by_month: Dict[str, Dict[str, float]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_income": 5000.0,
                "total_expenses": 3200.0,
                "net_flow": 1800.0,
                "by_category": {
                    "salary": 4000.0,
                    "freelance": 1000.0,
                    "groceries": 800.0,
                    "rent": 1200.0,
                    "utilities": 300.0,
                    "entertainment": 400.0,
                    "other": 500.0
                },
                "by_month": {
                    "2023-01": {"income": 5000.0, "expenses": 3200.0, "net": 1800.0},
                    "2023-02": {"income": 5000.0, "expenses": 3000.0, "net": 2000.0}
                }
            }
        }