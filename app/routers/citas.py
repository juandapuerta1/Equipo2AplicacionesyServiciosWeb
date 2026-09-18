from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Ajustaremos este import cuando configuremos la BD
from app.core.database import get_db 
from app.schemas.cita import CitaCreate, CitaUpdate, CitaResponse
from app.repositories import cita as cita_repo

router = APIRouter(prefix="/citas", tags=["Citas de Uñas"])

@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    return cita_repo.crear(db=db, datos=cita)

@router.get("/", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return cita_repo.listar(db=db)

@router.get("/{cita_id}", response_model=CitaResponse)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = cita_repo.obtener_por_id(db=db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return db_cita

@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(cita_id: int, cita_datos: CitaUpdate, db: Session = Depends(get_db)):
    db_cita = cita_repo.obtener_por_id(db=db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita_repo.actualizar(db=db, cita=db_cita, datos=cita_datos)

@router.delete("/{cita_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    db_cita = cita_repo.obtener_por_id(db=db, cita_id=cita_id)
    if db_cita is None:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita_repo.eliminar(db=db, cita=db_cita)