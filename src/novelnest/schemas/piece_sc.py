from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict



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
    num_of_likes: int = 0
    
    model_config = ConfigDict(from_attributes=True)
