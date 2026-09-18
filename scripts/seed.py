import os
import sys

# Agregar la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine, Base
from app.models.producto import Producto


def run_seed():
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Lista de productos de prueba para el seeder
        productos_semilla = [
            {
                "nombre": "Laptop Gamer Pro",
                "descripcion": "Intel i7, 16GB RAM, RTX 3060",
                "precio": 1200.00,
                "stock": 15,
            },
            {
                "nombre": "Mouse Inalámbrico",
                "descripcion": "Ergonómico con sensor óptico",
                "precio": 25.50,
                "stock": 50,
            },
            {
                "nombre": "Teclado Mecánico RGB",
                "descripcion": "Switches Red, retroiluminado",
                "precio": 75.00,
                "stock": 30,
            },
        ]

        nuevos_agregados = 0
        for p in productos_semilla:
            # Verifica si el producto ya existe por el nombre
            existe = db.query(Producto).filter(Producto.nombre == p["nombre"]).first()
            if not existe:
                nuevo_prod = Producto(
                    nombre=p["nombre"],
                    descripcion=p["descripcion"],
                    precio=p["precio"],
                    stock=p["stock"],
                )
                db.add(nuevo_prod)
                nuevos_agregados += 1

        db.commit()
        print(
            f"Seeder completado con éxito. Se agregaron {nuevos_agregados} productos nuevos."
        )
    except Exception as e:
        db.rollback()
        print(f"Error al ejecutar el seeder: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
