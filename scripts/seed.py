"""Script para migrar tablas y poblar datos iniciales (seeders)."""

from app.core.database import Base, engine, SessionLocal
from app.models.producto import Producto


def run_migrations_and_seeders():
    print("Conectando y creando tablas en PostgreSQL Neon...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        conteo = db.query(Producto).count()
        print(f"Registros actuales en la tabla 'productos': {conteo}")

        if conteo == 0:
            print("Insertando seeders de Producto...")
            productos_iniciales = [
                Producto(
                    nombre="Teclado Mecánico RGB",
                    descripcion="Teclado switches red con iluminación RGB",
                    precio=250000.0,
                    stock=12,
                    disponible=True,
                ),
                Producto(
                    nombre="Mouse Gamer Ergonómico",
                    descripcion="Mouse con sensor óptico 16000 DPI",
                    precio=120000.0,
                    stock=20,
                    disponible=True,
                ),
                Producto(
                    nombre="Monitor Curvo 27",
                    descripcion="Monitor 144Hz 1ms para juegos",
                    precio=950000.0,
                    stock=5,
                    disponible=True,
                ),
            ]
            db.add_all(productos_iniciales)
            db.commit()
            print("¡Seeders aplicados correctamente!")
        else:
            print(
                "La base de datos ya contiene registros. Omitiendo la siembra de datos."
            )

    except Exception as error:
        db.rollback()
        print(f"Error durante la migración o ejecución del seeder: {error}")
        raise error
    finally:
        db.close()


if __name__ == "__main__":
    run_migrations_and_seeders()
