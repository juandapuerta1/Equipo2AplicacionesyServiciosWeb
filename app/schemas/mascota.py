from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class MascotaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    especie: str = Field(..., min_length=3, max_length=30)
    raza: Optional[str] = None
    edad: int = Field(..., ge=0, le=40)
    peso: Optional[float] = Field(None, gt=0)
    vacunado: bool = False


class MascotaCreate(MascotaBase):
    pass


class MascotaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    especie: Optional[str] = Field(None, min_length=3, max_length=30)
    raza: Optional[str] = None
    edad: Optional[int] = Field(None, ge=0, le=40)
    peso: Optional[float] = Field(None, gt=0)
    vacunado: Optional[bool] = None


class MascotaResponse(MascotaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
