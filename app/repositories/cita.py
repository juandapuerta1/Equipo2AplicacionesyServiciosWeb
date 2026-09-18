from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.cita import Cita
from app.schemas.cita import CitaCreate, CitaUpdate

def listar(db: Session) -> list[Cita]:
    return list(db.scalars(select(Cita).order_by(Cita.fecha_hora)))

def obtener_por_id(db: Session, cita_id: int) -> Cita | None:
    return db.get(Cita, cita_id)

def crear(db: Session, datos: CitaCreate) -> Cita:
    cita = Cita(
        nombre_cliente=datos.nombre_cliente,
        servicio=datos.servicio,
        fecha_hora=datos.fecha_hora,
        estado=datos.estado
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita

def actualizar(
    db: Session, cita: Cita, datos: CitaUpdate
) -> Cita:
    if datos.nombre_cliente is not None:
        cita.nombre_cliente = datos.nombre_cliente
    if datos.servicio is not None:
        cita.servicio = datos.servicio
    if datos.fecha_hora is not None:
        cita.fecha_hora = datos.fecha_hora
    if datos.estado is not None:
        cita.estado = datos.estado
        
    db.commit()
    db.refresh(cita)
    return cita

def eliminar(db: Session, cita: Cita) -> None:
    db.delete(cita)
    db.commit()