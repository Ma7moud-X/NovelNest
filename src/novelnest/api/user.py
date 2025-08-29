from typing import List, Annotated

from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..schemas import user_sc
from ..core import OAuth2
from ..core.database import get_db
from ..models import user_t

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/", response_model=List[user_sc.User])
def get_all_users(db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0):
    users = db.query(user_t.User).limit(limit).offset(offset).all()
    return users

@router.get("/{id}", response_model=user_sc.User)
def get_user_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(user_t.User).filter(user_t.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")

    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_sc.User)
def create_user(user: user_sc.UserCreate, db: Annotated[Session, Depends(get_db)]):
    
    same_username_or_email = db.query(user_t.User).filter(or_(user_t.User.username == user.username, user_t.User.email == user.email)).first()

    if same_username_or_email:
        if same_username_or_email.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username '{user.username}' is already taken.")
        if same_username_or_email.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{user.email}' is already in use.")

    
    user.password = OAuth2.hash_password(user.password)
        
    new_user = user_t.User(**user.model_dump(), role = user_sc.UserRole.USER)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # to get db generated values
    return new_user

@router.post("/admin", status_code=status.HTTP_201_CREATED, response_model=user_sc.User)
def create_admin_user(user: user_sc.UserCreate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_admin_user)]):

    same_username_or_email = db.query(user_t.User).filter(or_(user_t.User.username == user.username, user_t.User.email == user.email)).first()

    if same_username_or_email:
        if same_username_or_email.username == user.username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username '{user.username}' is already taken.")
        if same_username_or_email.email == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{user.email}' is already in use.")
    
    user.password = OAuth2.hash_password(user.password)
        
    new_user = user_t.User(**user.model_dump(), role = user_sc.UserRole.ADMIN)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # to get db generated values
    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_user)]):
    
    OAuth2.require_admin_or_self(id, current_user)

    user = db.query(user_t.User).filter(user_t.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
    db.delete(user)
    db.commit()

@router.put("/{id}", response_model=user_sc.User)
def update_user(id: int, new_user: user_sc.UserUpdate, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_user)]):
    user_query = db.query(user_t.User).filter(user_t.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")

    # Check if user can access this data
    OAuth2.require_admin_or_self(id, current_user)

    update_data = new_user.model_dump(exclude_unset=True)
    user_update_data = new_user.model_dump(exclude_unset=True, exclude={'role'})
    
    # Only admins can change roles
    if new_user.role != None and current_user.role != user_sc.UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only admins can change user roles"
        )
        
    # No fields to update, return the user as is
    if not update_data: 
        return user 

    # Admins acn only change roles
    if user_update_data:
        OAuth2.require_self(id, current_user)


    conflict_query = db.query(user_t.User).filter(user_t.User.id != id)
        
    if new_user.username != None:
        existing_username = conflict_query.filter(user_t.User.username == update_data['username']).first()
        if existing_username:   
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username '{new_user.username}' is already taken.")

    if new_user.email != None:
        existing_email = conflict_query.filter(user_t.User.email == update_data['email']).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{new_user.email}' is already in use.")
        
    if new_user.password != None:
        new_user.password = OAuth2.hash_password(new_user.password)
    
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    
    db.refresh(user)
    return user