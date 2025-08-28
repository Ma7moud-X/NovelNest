from sqlalchemy import TIMESTAMP, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from ..core.database import Base

 
class Piece(Base):
    __tablename__ = "pieces"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    num_of_likes = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    liked_by_users = relationship("User", secondary="likes", back_populates="liked_pieces")
 