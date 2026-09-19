from sqlalchemy.orm import Session
from app.models.games import Videojuego
from app.schemas.games import VideojuegoCreate, VideojuegoUpdate


def crear_videojuego(db: Session, videojuego: VideojuegoCreate):
    db_videojuego = Videojuego(**videojuego.model_dump())
    db.add(db_videojuego)
    db.commit()
    db.refresh(db_videojuego)
    return db_videojuego


def obtener_videojuegos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Videojuego).offset(skip).limit(limit).all()


def obtener_videojuego_por_id(db: Session, videojuego_id: int):
    return db.query(Videojuego).filter(Videojuego.id == videojuego_id).first()


def actualizar_videojuego(
    db: Session, videojuego_id: int, videojuego_data: VideojuegoUpdate
):
    db_videojuego = obtener_videojuego_por_id(db, videojuego_id)
    if not db_videojuego:
        return None

    update_dict = videojuego_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_videojuego, key, value)

    db.commit()
    db.refresh(db_videojuego)
    return db_videojuego


def eliminar_videojuego(db: Session, videojuego_id: int):
    db_videojuego = obtener_videojuego_por_id(db, videojuego_id)
    if not db_videojuego:
        return None

    db.delete(db_videojuego)
    db.commit()
    return db_videojuego