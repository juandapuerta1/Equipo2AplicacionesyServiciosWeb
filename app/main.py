from fastapi import FastAPI
from app.routers import games

app = FastAPI(title="API Tienda Videojuegos")

app.include_router(games.router)