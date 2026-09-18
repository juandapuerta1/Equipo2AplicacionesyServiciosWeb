from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate


def listar(db: Session) -> list[Mascota]:
    return list(db.scalars(select(Mascota).order_by(Mascota.nombre)))


def obtener_por_id(db: Session, mascota_id: int) -> Mascota | None:
    return db.get(Mascota, mascota_id)


def crear(db: Session, datos: MascotaCreate) -> Mascota:
    mascota = Mascota(
        nombre=datos.nombre,
        especie=datos.especie,
        raza=datos.raza,
        edad=datos.edad,
        peso=datos.peso,
        vacunado=datos.vacunado,
    )
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota


def actualizar(db: Session, mascota: Mascota, datos: MascotaUpdate) -> Mascota:
    if datos.nombre is not None:
        mascota.nombre = datos.nombre
    if datos.especie is not None:
        mascota.especie = datos.especie
    if datos.raza is not None:
        mascota.raza = datos.raza
    if datos.edad is not None:
        mascota.edad = datos.edad
    if datos.peso is not None:
        mascota.peso = datos.peso
    if datos.vacunado is not None:
        mascota.vacunado = datos.vacunado

    db.commit()
    db.refresh(mascota)
    return mascota


def eliminar(db: Session, mascota: Mascota) -> None:
    db.delete(mascota)
    db.commit()
