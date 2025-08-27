from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database import get_db
from .. import api_schemas, db_models

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=List[api_schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(db_models.User).all()
    return users

@router.get("/{id}", response_model=api_schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")

    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=api_schemas.User)
def create_user(user: api_schemas.UserCreate, db: Session = Depends(get_db)):
    
    same_username_or_email = db.query(db_models.User).filter(
        or_(db_models.User.username == user.username, db_models.User.email == user.email)
    ).first()

    if same_username_or_email:
        if same_username_or_email.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username '{user.username}' is already taken.")
        if same_username_or_email.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{user.email}' is already in use.")
    
    
    new_user = db_models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # to get db generated values
    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(db_models.User).filter(db_models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
    db.delete(user)
    db.commit()

@router.put("/{id}", response_model=api_schemas.User)
def update_user(id: int, new_user: api_schemas.UserUpdate, db: Session = Depends(get_db)):
    
    user_query = db.query(db_models.User).filter(db_models.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")

    update_data = new_user.model_dump(exclude_unset=True)
    
    # No fields to update, return the user as is
    if not update_data: 
        return user 

    conflict_query = db.query(db_models.User).filter(db_models.User.id != id)
        
    if new_user.username != None:
        existing_username = conflict_query.filter(db_models.User.username == update_data['username']).first()
        if existing_username:   
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username '{new_user.username}' is already taken.")

    if new_user.email != None:
        existing_email = conflict_query.filter(db_models.User.email == update_data['email']).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{new_user.email}' is already in use.")
    
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    
    db.refresh(user)
    return user
















###########################################################
## test all in here before watching the vid  ##############
###########################################################