from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, Enum
from sqlalchemy.sql.expression import text
from .database import Base
from .api_schemas import UserRole

class Piece(Base):
    __tablename__ = "pieces"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
    