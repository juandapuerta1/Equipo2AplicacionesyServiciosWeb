from pydantic import BaseModel, Field
from typing import Optional


class VideojuegoBase(BaseModel):
    titulo: str = Field(
        ..., min_length=2, max_length=100, description="Título del videojuego"
    )
    genero: str = Field(
        ..., min_length=2, max_length=50, description="Género del videojuego"
    )
    desarrollador: Optional[str] = Field(
        None, max_length=100, description="Estudio o desarrollador del videojuego"
    )
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    disponible: bool = True


class VideojuegoCreate(VideojuegoBase):
    pass


class VideojuegoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=2, max_length=100)
    genero: Optional[str] = Field(None, min_length=2, max_length=50)
    desarrollador: Optional[str] = Field(None, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None


class VideojuegoResponse(VideojuegoBase):
    id: int

    class Config:
        from_attributes = True