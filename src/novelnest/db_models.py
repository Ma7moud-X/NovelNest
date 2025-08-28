from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
from .api_schemas import UserRole

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    liked_pieces = relationship("Piece", secondary="likes", back_populates="liked_by_users")
    
    
class Piece(Base):
    __tablename__ = "pieces"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    num_of_likes = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    liked_by_users = relationship("User", secondary="likes", back_populates="liked_pieces")
    

class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    piece_id = Column(Integer, ForeignKey("pieces.id", ondelete="CASCADE"), primary_key=True)
