from sqlalchemy import TIMESTAMP, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from ..api_schemas.user import UserRole
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    liked_pieces = relationship("Piece", secondary="likes", back_populates="liked_by_users")
    