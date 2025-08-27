from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BasePiece(BaseModel):
    title: str
    description: Optional[str] = ""

class AddPiece(BasePiece):
    pass

class UpdatePiece(BasePiece):
    pass

class Piece(BasePiece):
    id: int
    created_at: datetime




