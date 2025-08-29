from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    # is_verified: bool = False 
    
class User(BaseUser):
    id: int
    created_at: datetime
    role: UserRole = UserRole.USER
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseUser):
    password: str

class UserLogin(BaseModel):
    username: str  # Only need username/email and password for login
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
