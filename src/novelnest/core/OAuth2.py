from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..api_schemas import auth as sc_auth
from ..api_schemas import user as sc_user
from ..core import database
from ..db_models import user as db_user
from .config import settings



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algo)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algo])
        user_id: str = payload.get("user_id")
        if user_id is None:
            logger.warning("Token missing user_id")
            raise credentials_exception
        token_data = sc_auth.TokenData(id=str(user_id))
        return token_data
    except InvalidTokenError as e:
        raise credentials_exception
    except Exception as e:
        raise credentials_exception

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(database.get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(db_user.User).filter(db_user.User.id == token_data.id).first()
    
    if not user:
        raise credentials_exception
    
    return user

def get_current_admin_user(current_user: Annotated[db_user.User, Depends(get_current_user)]):
    if current_user.role != sc_user.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_admin_or_self(user_id: int, current_user: Annotated[db_user.User, Depends(get_current_user)]):
    if current_user.role != sc_user.UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin access required or you can only access your own data"
        )
    return current_user

def require_self(user_id: int, current_user: Annotated[db_user.User, Depends(get_current_user)]):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access or change your own data"
        )
    return current_user