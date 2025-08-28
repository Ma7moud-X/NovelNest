from fastapi import status, HTTPException, APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import api_schemas, db_models, OAuth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=api_schemas.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):  # In Postman, the inputs are in form-data, not raw JSON

    user = db.query(db_models.User).filter( 
        db_models.User.username == user_credentials.username).first()

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

    return api_schemas.Token(access_token=access_token, token_type="bearer")