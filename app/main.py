from fastapi import FastAPI
from app.core.database import Base, engine

# Importes de Alejandro (Producto)
from app.routers import producto as producto_router
from app.models import producto as producto_model

# Importes de main (Mascota y Citas)
from app.routers import mascota
from app.routers import citas

# Esto crea las tablas en Neon automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Equipo 2")

# Registrando los endpoints del CRUD de todos los integrantes
app.include_router(producto_router.router)
app.include_router(mascota.router)
app.include_router(citas.router)