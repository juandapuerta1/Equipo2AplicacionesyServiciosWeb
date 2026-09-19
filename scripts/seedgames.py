import os
import sys

# Agregar la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import Base, SessionLocal, engine
from app.models.games import Videojuego


def run_seed():
    # Crear las tablas si no existen en la base de datos
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Lista de videojuegos de prueba con precios en COP
        videojuegos_semilla = [
            {
                "titulo": "The Legend of Zelda: Tears of the Kingdom",
                "genero": "Aventura",
                "desarrollador": "Nintendo",
                "precio": 319900.0,
                "stock": 25,
                "disponible": True,
            },
            {
                "titulo": "God of War Ragnarök",
                "genero": "Acción",
                "desarrollador": "Santa Monica Studio",
                "precio": 289900.0,
                "stock": 18,
                "disponible": True,
            },
            {
                "titulo": "Elden Ring",
                "genero": "RPG",
                "desarrollador": "FromSoftware",
                "precio": 239900.0,
                "stock": 30,
                "disponible": True,
            },
            {
                "titulo": "Cyberpunk 2077",
                "genero": "RPG",
                "desarrollador": "CD Projekt Red",
                "precio": 189900.0,
                "stock": 0,
                "disponible": False,
            },
        ]

        nuevos_agregados = 0
        for juego in videojuegos_semilla:
            # Verifica si el videojuego ya existe por el título
            existe = (
                db.query(Videojuego)
                .filter(Videojuego.titulo == juego["titulo"])
                .first()
            )
            if not existe:
                nuevo_juego = Videojuego(
                    titulo=juego["titulo"],
                    genero=juego["genero"],
                    desarrollador=juego["desarrollador"],
                    precio=juego["precio"],
                    stock=juego["stock"],
                    disponible=juego["disponible"],
                )
                db.add(nuevo_juego)
                nuevos_agregados += 1

        db.commit()
        print(
            f"Seeder completado con éxito. Se agregaron {nuevos_agregados} videojuegos nuevos."
        )
    except Exception as e:
        db.rollback()
        print(f"Error al ejecutar el seeder: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()