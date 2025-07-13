from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum

class UserType(str, Enum):
    ops = "ops"
    client = "client"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: UserType

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    user_type: UserType
    is_verified: bool

    class Config:
        from_attributes = True