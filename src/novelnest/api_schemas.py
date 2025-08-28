from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class BasePiece(BaseModel):
    title: str
    description: Optional[str] = None

class AddPiece(BasePiece):
    pass

class UpdatePiece(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class Piece(BasePiece):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

#################################################################

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

#################################################################
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

#################################################################
class LikeToggle(BaseModel):
    piece_id: int
    direction: int = 1  # 1 = like, 0 = unlike (remove)
    
    @field_validator('direction')
    @classmethod
    def validate_direction(cls, v):
        if v not in [0, 1]:
            raise ValueError('direction must be either 0 (unlike) or 1 (like)')
        return v

class Like(BaseModel):
    piece_id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class LikeCount(BaseModel):
    piece_id: int
    like_count: int