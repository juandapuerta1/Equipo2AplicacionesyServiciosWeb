from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CitaBase(BaseModel):
    nombre_cliente: str
    servicio: str
    fecha_hora: datetime
    estado: Optional[str] = "Agendada"

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    nombre_cliente: Optional[str] = None
    servicio: Optional[str] = None
    fecha_hora: Optional[datetime] = None
    estado: Optional[str] = None

class CitaResponse(CitaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)