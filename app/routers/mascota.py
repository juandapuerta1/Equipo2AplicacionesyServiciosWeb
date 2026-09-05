from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaResponse
from app.repositories import mascota as mascota_repo

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


@router.post("/", response_model=MascotaResponse, status_code=status.HTTP_201_CREATED)
def crear_mascota(mascota: MascotaCreate, db: Session = Depends(get_db)):
    return mascota_repo.crear(db=db, datos=mascota)


@router.get("/", response_model=list[MascotaResponse])
def listar_mascotas(db: Session = Depends(get_db)):
    return mascota_repo.listar(db=db)


@router.get("/{mascota_id}", response_model=MascotaResponse)
def obtener_mascota(mascota_id: int, db: Session = Depends(get_db)):
    db_mascota = mascota_repo.obtener_por_id(db=db, mascota_id=mascota_id)
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return db_mascota


@router.put("/{mascota_id}", response_model=MascotaResponse)
def actualizar_mascota(
    mascota_id: int, mascota_datos: MascotaUpdate, db: Session = Depends(get_db)
):
    db_mascota = mascota_repo.obtener_por_id(db=db, mascota_id=mascota_id)
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return mascota_repo.actualizar(db=db, mascota=db_mascota, datos=mascota_datos)


@router.delete("/{mascota_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mascota(mascota_id: int, db: Session = Depends(get_db)):
    db_mascota = mascota_repo.obtener_por_id(db=db, mascota_id=mascota_id)
    if db_mascota is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    mascota_repo.eliminar(db=db, mascota=db_mascota)
