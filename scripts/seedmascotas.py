import os
import sys

# Agregar la raiz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine, Base
from app.models.mascota import Mascota


def run_seed():
    # Crear las tablas en Neon si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        mascotas_semilla = [
            {
                "nombre": "Firulais",
                "especie": "Perro",
                "raza": "Labrador",
                "edad": 3,
                "peso": 15.5,
                "vacunado": True,
            },
            {
                "nombre": "Michi",
                "especie": "Gato",
                "raza": "Siames",
                "edad": 2,
                "peso": 4.2,
                "vacunado": True,
            },
            {
                "nombre": "Rocky",
                "especie": "Perro",
                "raza": "Bulldog",
                "edad": 5,
                "peso": 22.0,
                "vacunado": False,
            },
        ]

        nuevos_agregados = 0
        for m in mascotas_semilla:
            existe = db.query(Mascota).filter(Mascota.nombre == m["nombre"]).first()
            if not existe:
                nueva_mascota = Mascota(
                    nombre=m["nombre"],
                    especie=m["especie"],
                    raza=m["raza"],
                    edad=m["edad"],
                    peso=m["peso"],
                    vacunado=m["vacunado"],
                )
                db.add(nueva_mascota)
                nuevos_agregados += 1

        db.commit()
        print(
            f"Seeder completado con exito. Se agregaron {nuevos_agregados} mascotas nuevas."
        )
    except Exception as e:
        db.rollback()
        print(f"Error al ejecutar el seeder: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
