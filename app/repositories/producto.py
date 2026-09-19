from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).offset(skip).limit(limit).all()


def get_producto_by_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()


def update_producto(db: Session, producto_id: int, producto_data: ProductoUpdate):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None

    update_dict = producto_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None
    db.delete(db_producto)
    db.commit()
    return db_producto
