from typing import Annotated

from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..api_schemas import auth as sc_auth
from ..core import OAuth2
from ..core.database import get_db
from ..db_models import user as db_user

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=sc_auth.Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):  # In Postman, the inputs are in form-data, not raw JSON

    user = db.query(db_user.User).filter( 
        db_user.User.username == user_credentials.username).first()

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

    return sc_auth.Token(access_token=access_token, token_type="bearer")