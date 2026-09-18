"""Comprueba que la base de datos responda. Lo usa el workflow de CI."""

import sys
from sqlalchemy import text
from app.core.database import engine


def main() -> int:
    try:
        with engine.connect() as conexion:
            version = conexion.execute(text("SELECT version()")).scalar()
    except Exception as error:
        print(f"ERROR: no se pudo conectar a la base de datos -> {error}")
        return 1

    print(f"Conexión correcta. PostgreSQL: {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
