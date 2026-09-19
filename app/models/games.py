from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base


class Videojuego(Base):
    __tablename__ = "videojuegos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, index=True)
    genero = Column(String, nullable=False, index=True)
    desarrollador = Column(String, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)