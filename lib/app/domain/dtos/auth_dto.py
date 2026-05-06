from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    name:     str
    email:    EmailStr
    password: str
    phone:    Optional[str] = None


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      str
    phone:      Optional[str]
    role:       str
    created_at: datetime

    class Config:
        from_attributes = True