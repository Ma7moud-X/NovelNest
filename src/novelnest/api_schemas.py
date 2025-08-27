from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional


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
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseUser):
    password: str

class UserLogin(BaseUser):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     id: Optional[str] = None