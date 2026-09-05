from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import mascota
from app.routers import citas

# Esto crea la tabla en Neon automáticamente si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Equipo 2")

# Registrando los endpoints del CRUD
app.include_router(mascota.router)
app.include_router(citas.router)