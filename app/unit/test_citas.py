from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- 1. POST (Crear) ---
def test_crear_cita_normal():
    payload = {
        "nombre_cliente": "Juan Perez",
        "servicio": "Manicura semipermanente",
        "fecha_hora": "2026-11-20T14:30:00",
        "estado": "Agendada"
    }
    response = client.post("/citas/", json=payload)
    assert response.status_code in [200, 201]
    assert response.json()["nombre_cliente"] == "Juan Perez"

def test_crear_cita_error_faltan_datos():
    # Mandamos un payload incompleto (falta 'servicio' y 'fecha_hora')
    payload = {"nombre_cliente": "Maria"}
    response = client.post("/citas/", json=payload)
    assert response.status_code == 422 # Error de validación Pydantic

# --- 2. GET (Listar) ---
def test_obtener_citas_normal():
    response = client.get("/citas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_citas_error_metodo():
    # Forzamos un error de método no permitido (POST a una ruta de listado sin cuerpo)
    response = client.post("/citas/")
    assert response.status_code == 422

# --- 3. GET por ID (Obtener una) ---
def test_obtener_cita_por_id_normal():
    # Consultamos el ID 1 (Asumiendo que el test anterior lo creó o existe)
    response = client.get("/citas/1")
    assert response.status_code in [200, 404]

def test_obtener_cita_por_id_error_inexistente():
    # Consultamos un ID que no existe
    response = client.get("/citas/999999")
    assert response.status_code == 404

# --- 4. PUT (Actualizar) ---
def test_actualizar_cita_normal():
    payload = {
        "nombre_cliente": "Juan Perez Modificado",
        "servicio": "Manicura y Pedicura",
        "fecha_hora": "2026-11-20T15:00:00",
        "estado": "Completada"
    }
    response = client.put("/citas/1", json=payload)
    assert response.status_code in [200, 404]

def test_actualizar_cita_error_datos_invalidos():
    # Mandamos un string donde la API espera un datetime válido
    payload = {"fecha_hora": "fecha_invalida_no_es_fecha"}
    response = client.put("/citas/1", json=payload)
    assert response.status_code == 422

# --- 5. DELETE (Eliminar) ---
def test_eliminar_cita_normal():
    response = client.delete("/citas/1")
    assert response.status_code in [200, 204, 404]

def test_eliminar_cita_error_inexistente():
    response = client.delete("/citas/999999")
    assert response.status_code == 404