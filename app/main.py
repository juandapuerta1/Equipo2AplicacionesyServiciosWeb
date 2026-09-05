from fastapi import FastAPI
from app.core.database import Base, engine

# 1. Importar el router desde app.routers (contiene las rutas/endpoints)
from app.routers import producto as producto_router

# 2. Importar el modelo desde app.models (para que SQLAlchemy cree las tablas)
from app.models import producto as producto_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API")

# 3. Registrar el router correcto
app.include_router(producto_router.router)
