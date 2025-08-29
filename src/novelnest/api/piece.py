from typing import List, Annotated, Optional

from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import piece_sc
from ..core import OAuth2
from ..core.database import get_db
from ..models import piece_t, user_t


router = APIRouter(
    prefix="/pieces",
    tags=['Pieces']
)


@router.get("/", response_model=List[piece_sc.Piece])
def get_all_pieces(db: Annotated[Session, Depends(get_db)], limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    pieces = db.query(piece_t.Piece).filter(piece_t.Piece.title.contains(search)).limit(limit).offset(offset).all()
    return pieces

@router.get("/{id}", response_model=piece_sc.Piece)
def get_piece_by_id(id: int, db: Annotated[Session, Depends(get_db)]):
    piece = db.query(piece_t.Piece).filter(piece_t.Piece.id == id).first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")

    return piece

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=piece_sc.Piece)
def create_piece(piece: piece_sc.AddPiece, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_admin_user)]):
    new_piece = piece_t.Piece(**piece.model_dump())
    db.add(new_piece)
    db.commit()
    db.refresh(new_piece) # to get db generated values
    return new_piece

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_piece(id: int, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_admin_user)]):
    piece = db.query(piece_t.Piece).filter(piece_t.Piece.id == id).first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")
    
    db.delete(piece)
    db.commit()

@router.put("/{id}", response_model=piece_sc.Piece)
def update_piece(id: int, new_piece: piece_sc.UpdatePiece, db: Annotated[Session, Depends(get_db)], current_user: Annotated[user_t.User, Depends(OAuth2.get_current_admin_user)]):
    piece_query = db.query(piece_t.Piece).filter(piece_t.Piece.id == id)
    piece = piece_query.first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")
    
    update_data = new_piece.model_dump(exclude_unset=True)
    
    # No fields to update, return the piece as is
    if not update_data: 
        return piece 
    
    piece_query.update(update_data, synchronize_session=False)
    db.commit()
    
    db.refresh(piece)
    return piece