from pydantic import BaseModel, EmailStr
from .models import UserRole

# Schema for token data
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# Base schema for User properties
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.user

# Schema for creating a new user
class UserCreate(UserBase):
    password: str

# Schema for reading user data (excluding password)
class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True