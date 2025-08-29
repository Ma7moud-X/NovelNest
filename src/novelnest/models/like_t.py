from sqlalchemy import Column, ForeignKey, Integer
from ..core.database import Base


class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    piece_id = Column(Integer, ForeignKey("pieces.id", ondelete="CASCADE"), primary_key=True)
