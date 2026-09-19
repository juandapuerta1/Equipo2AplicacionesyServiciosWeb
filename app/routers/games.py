from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.games import VideojuegoCreate, VideojuegoUpdate, VideojuegoResponse
import app.repositories.games as videojuego_repo

router = APIRouter(prefix="/videojuegos", tags=["Videojuegos"])


@router.post("/", response_model=VideojuegoResponse, status_code=status.HTTP_201_CREATED)
def crear_videojuego(videojuego: VideojuegoCreate, db: Session = Depends(get_db)):
    return videojuego_repo.crear_videojuego(db=db, videojuego=videojuego)


@router.get("/", response_model=List[VideojuegoResponse])
def listar_videojuegos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return videojuego_repo.obtener_videojuegos(db=db, skip=skip, limit=limit)


@router.get("/{videojuego_id}", response_model=VideojuegoResponse)
def obtener_videojuego(videojuego_id: int, db: Session = Depends(get_db)):
    db_videojuego = videojuego_repo.obtener_videojuego_por_id(db, videojuego_id=videojuego_id)
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return db_videojuego


@router.put("/{videojuego_id}", response_model=VideojuegoResponse)
def actualizar_videojuego(
    videojuego_id: int, videojuego: VideojuegoUpdate, db: Session = Depends(get_db)
):
    db_videojuego = videojuego_repo.actualizar_videojuego(
        db=db, videojuego_id=videojuego_id, videojuego_data=videojuego
    )
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return db_videojuego


@router.delete("/{videojuego_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_videojuego(videojuego_id: int, db: Session = Depends(get_db)):
    db_videojuego = videojuego_repo.eliminar_videojuego(db=db, videojuego_id=videojuego_id)
    if not db_videojuego:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return None