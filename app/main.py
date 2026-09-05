from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import citas, games

# 🔴 Comenta esta línea temporalmente
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Tienda Videojuegos")

app.include_router(citas.router)
app.include_router(games.router)