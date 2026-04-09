from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdateRole(BaseModel):
    role: str = Field(..., pattern="^(admin|analyst|viewer)$")

class UserUpdateStatus(BaseModel):
    is_active: bool

class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True)
