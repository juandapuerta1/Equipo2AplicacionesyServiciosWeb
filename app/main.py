import time
from sqlalchemy.exc import OperationalError
from fastapi import FastAPI
from app.core.database import Base, engine

# Import de tu módulo (Videojuegos)
from app.routers import games

# Importes de Alejandro (Producto)
from app.routers import producto as producto_router
from app.models import producto as producto_model

# Importes de otros integrantes (Mascota y Citas)
from app.routers import mascota
from app.routers import citas

# Esto crea las tablas en Neon automáticamente si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Equipo 2")

# Bucle de reintentos para esperar a que PostgreSQL esté listo en Docker
max_retries = 5
retry_interval = 2

for attempt in range(max_retries):
    try:
        Base.metadata.create_all(bind=engine)
        print("¡Conexión a la base de datos establecida con éxito!")
        break
    except OperationalError:
        if attempt < max_retries - 1:
            print(
                f"Base de datos no lista, reintentando en {retry_interval}s... (Intento {attempt + 1}/{max_retries})"
            )
            time.sleep(retry_interval)
        else:
            raise

# Registrando los endpoints del CRUD de todos los integrantes
app.include_router(games.router)
app.include_router(producto_router.router)
app.include_router(mascota.router)
app.include_router(citas.router)
