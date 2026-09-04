from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import citas

# Esto crea la tabla en Neon automáticamente si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Agendamiento de Uñas")

# Registrando los endpoints del CRUD
app.include_router(citas.router)