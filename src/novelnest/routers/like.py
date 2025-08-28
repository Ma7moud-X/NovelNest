from fastapi import Response, status, HTTPException, APIRouter, Depends
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session

from ..database import get_db
from .. import api_schemas, db_models, OAuth2

router = APIRouter(
    prefix="/likes",
    tags=['Likes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def toggle_like(like_data: api_schemas.LikeToggle, db: Annotated[Session, Depends(get_db)], current_user: Annotated[db_models.User, Depends(OAuth2.get_current_user)]):
    
    piece = db.query(db_models.Piece).filter(db_models.Piece.id == like_data.piece_id).first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id: {like_data.piece_id} does not exist")
     
    like_query = db.query(db_models.Like).filter(db_models.Like.piece_id == like_data.piece_id, db_models.Like.user_id == current_user.id)
    found_like = like_query.first()
    
    if like_data.direction == 1:  # User wants to like
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already liked piece {like_data.piece_id}")
        
        # Add the like
        new_like = db_models.Like(piece_id=like_data.piece_id, user_id=current_user.id)
        db.add(new_like)
        
        # Increment the like count
        piece.num_of_likes += 1
        
        db.commit()
        db.refresh(new_like)
        
        return {"message": "Successfully added like", "like": new_like}
        
    else:  # direction == 0, user wants to unlike
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")

        # Remove the like
        like_query.delete(synchronize_session=False)
        
        # Decrement the like count (but don't go below 0)
        if piece.num_of_likes > 0:
            piece.num_of_likes -= 1
        
        db.commit()
        
        return {"message": "Successfully removed like"}
    
@router.get("/count/{piece_id}", response_model=api_schemas.LikeCount)
def get_like_count(piece_id: int, db: Annotated[Session, Depends(get_db)]):
    piece = db.query(db_models.Piece).filter(db_models.Piece.id == piece_id).first()
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id: {piece_id} does not exist")
    
    count = db.query(db_models.Like).filter(db_models.Like.piece_id == piece_id).count()
    return {"piece_id": piece_id, "like_count": count}

@router.get("/my-likes", response_model=List[api_schemas.Like])
def get_my_likes(db: Annotated[Session, Depends(get_db)], current_user: Annotated[db_models.User, Depends(OAuth2.get_current_user)], limit: int = 10, offset: int = 0):    
    likes = db.query(db_models.Like).filter(db_models.Like.user_id == current_user.id).limit(limit).offset(offset).all()
    return likes
    
@router.get("/{piece_id}", response_model=List[api_schemas.Like])
def get_likes_for_piece(piece_id: int, db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0):    
    piece = db.query(db_models.Piece).filter(db_models.Piece.id == piece_id).first()
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id: {piece_id} does not exist")
    
    likes = db.query(db_models.Like).filter(db_models.Like.piece_id == piece_id).limit(limit).offset(offset).all()
    return likes

