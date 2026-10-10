from fastapi import FastAPI
from app.core.database import Base, engine

# Tu router de Videojuegos
from app.routers import games

# Importes de Alejandro (Producto)
from app.routers import producto as producto_router
from app.models import producto as producto_model

# Importes del resto del equipo (Mascota y Citas)
from app.routers import mascota
from app.routers import citas

# Crea las tablas en la base de datos Neon si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Equipo 2")

# Registro de los routers para cada módulo
app.include_router(games.router)
app.include_router(producto_router.router)
app.include_router(mascota.router)
app.include_router(citas.router)