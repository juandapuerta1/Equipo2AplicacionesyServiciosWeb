from pydantic import BaseModel, Field
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str = Field(
        ..., min_length=2, max_length=100, description="Nombre del producto"
    )
    descripcion: Optional[str] = Field(
        None, max_length=255, description="Descripción opcional"
    )
    precio: float = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True
