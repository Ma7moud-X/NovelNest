from fastapi import status, HTTPException, APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from .. import api_schemas, db_models

router = APIRouter(
    prefix="/pieces",
    tags=['Pieces']
)


@router.get("/", response_model=List[api_schemas.Piece])
def get_all_pieces(db: Session = Depends(get_db)):
    pieces = db.query(db_models.Piece).all()
    return pieces

@router.get("/{id}", response_model=api_schemas.Piece)
def get_piece_by_id(id: int, db: Session = Depends(get_db)):
    piece = db.query(db_models.Piece).filter(db_models.Piece.id == id).first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")

    return piece

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=api_schemas.Piece)
def create_piece(piece: api_schemas.AddPiece, db: Session = Depends(get_db)):
    new_piece = db_models.Piece(**piece.model_dump())
    db.add(new_piece)
    db.commit()
    db.refresh(new_piece) # to get db generated values
    return new_piece

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_piece(id: int, db: Session = Depends(get_db)):
    
    piece = db.query(db_models.Piece).filter(db_models.Piece.id == id).first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")
    
    db.delete(piece)
    db.commit()

@router.put("/{id}", response_model=api_schemas.Piece)
def update_piece(id: int, new_piece: api_schemas.UpdatePiece, db: Session = Depends(get_db)):
    
    piece_query = db.query(db_models.Piece).filter(db_models.Piece.id == id)
    piece = piece_query.first()
    
    if not piece:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Piece with id {id} was not found")
    
    update_data = new_piece.model_dump(exclude_unset=True)
    
    # No fields to update, return the user as is
    if not update_data: 
        return piece 
    
    piece_query.update(update_data, synchronize_session=False)
    db.commit()
    
    db.refresh(piece)
    return piece