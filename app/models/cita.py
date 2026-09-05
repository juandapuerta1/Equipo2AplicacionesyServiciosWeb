from sqlalchemy import Column, Integer, String, DateTime
# Ajustaremos este import cuando configuremos la conexión a Neon
from app.core.database import Base 

class Cita(Base):
    __tablename__ = "citas_unas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String, index=True, nullable=False)
    servicio = Column(String, nullable=False) 
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(String, default="Agendada")