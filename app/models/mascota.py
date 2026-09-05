from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    especie = Column(String(30), nullable=False)
    raza = Column(String(50), nullable=True)
    edad = Column(Integer, nullable=False)
    peso = Column(Float, nullable=True)
    vacunado = Column(Boolean, default=False)
