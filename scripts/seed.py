from app.core.database import Base, engine, SessionLocal
from app.models.producto import Producto


def run_migrations_and_seeders():
    print("Creando tablas en PostgreSQL Neon...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Verificar si ya existen productos para no duplicar
        if db.query(Producto).count() == 0:
            print("Insertando seeders de Producto...")
            productos_iniciales = [
                Producto(nombre="Teclado Mecánico", precio=150000.0, stock=10),
                Producto(nombre="Mouse Gamer", precio=85000.0, stock=15),
                Producto(nombre="Monitor 24 pulgadas", precio=650000.0, stock=5),
            ]
            db.add_all(productos_iniciales)
            db.commit()
            print("¡Seeders aplicados correctamente!")
        else:
            print("La base de datos ya contiene registros. Omitiendo seeders.")
    except Exception as e:
        db.rollback()
        print(f"Error durante el proceso: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_migrations_and_seeders()
