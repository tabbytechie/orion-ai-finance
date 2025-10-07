import datetime
from pydantic import BaseModel

# Base schema for Transaction properties
class TransactionBase(BaseModel):
    description: str | None = None
    amount: float
    category: str

# Schema for creating a new transaction
class TransactionCreate(TransactionBase):
    pass

# Schema for reading transaction data
class TransactionRead(TransactionBase):
    id: int
    date: datetime.datetime
    user_id: int

    class Config:
        from_attributes = True