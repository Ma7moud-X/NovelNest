from typing import Annotated

from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas import auth_sc
from ..core import OAuth2
from ..core.database import get_db
from ..models import user_t

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=auth_sc.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):  # In Postman, the inputs are in form-data, not raw JSON

    user = db.query(user_t.User).filter( 
        user_t.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )

    if not OAuth2.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )

    access_token = OAuth2.create_access_token(data={"user_id": user.id})

    return auth_sc.Token(access_token=access_token, token_type="bearer")