from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
import app.repositories.producto as producto_repo

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return producto_repo.create_producto(db=db, producto=producto)


@router.get("/", response_model=List[ProductoResponse])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return producto_repo.get_productos(db=db, skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto_repo.get_producto_by_id(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)
):
    db_producto = producto_repo.update_producto(
        db=db, producto_id=producto_id, producto_data=producto
    )
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = producto_repo.delete_producto(db=db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return None
