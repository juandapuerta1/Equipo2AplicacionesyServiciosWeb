import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ==========================================
# PRUEBAS EXITOSAS (5 pruebas)
# ==========================================


def test_01_crear_producto_exitoso():
    payload = {
        "nombre": "Teclado Mecánico",
        "descripcion": "Teclado RGB con switches red",
        "precio": 89.99,
        "stock": 15,
        "disponible": True,
    }
    response = client.post("/productos/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["precio"] == payload["precio"]
    assert "id" in data


def test_02_obtener_lista_productos_exitoso():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_03_obtener_producto_por_id_exitoso():
    # 1. Crear producto temporal
    payload = {
        "nombre": "Mouse Inalámbrico",
        "descripcion": "Mouse óptico ergonómico",
        "precio": 25.50,
        "stock": 30,
        "disponible": True,
    }
    create_res = client.post("/productos/", json=payload)
    assert create_res.status_code in [200, 201]
    prod_id = create_res.json()["id"]

    # 2. Consultar por ID
    response = client.get(f"/productos/{prod_id}")
    assert response.status_code == 200
    assert response.json()["id"] == prod_id


def test_04_actualizar_producto_exitoso():
    # 1. Crear producto temporal
    payload = {
        "nombre": "Monitor LED 24",
        "descripcion": "Monitor Full HD 75Hz",
        "precio": 120.00,
        "stock": 8,
        "disponible": True,
    }
    create_res = client.post("/productos/", json=payload)
    assert create_res.status_code in [200, 201]
    prod_id = create_res.json()["id"]

    # 2. Actualizar parcialmente
    update_payload = {"nombre": "Monitor LED 27 IPS", "precio": 180.00, "stock": 5}
    response = client.put(f"/productos/{prod_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["nombre"] == update_payload["nombre"]
    assert response.json()["precio"] == update_payload["precio"]


def test_05_eliminar_producto_exitoso():
    # 1. Crear producto temporal
    payload = {
        "nombre": "Audífonos Gamer",
        "descripcion": "Audífonos con micrófono",
        "precio": 45.00,
        "stock": 10,
        "disponible": True,
    }
    create_res = client.post("/productos/", json=payload)
    assert create_res.status_code in [200, 201]
    prod_id = create_res.json()["id"]

    # 2. Eliminar producto
    delete_res = client.delete(f"/productos/{prod_id}")
    assert delete_res.status_code in [200, 204]


# ==========================================
# PRUEBAS DE ERROR / VALIDACIÓN (5 pruebas)
# ==========================================


def test_06_crear_producto_precio_invalido_error():
    # Precio <= 0 rompe la regla gt=0 de Pydantic
    payload_invalido = {"nombre": "Producto Precio Cero", "precio": 0.0, "stock": 5}
    response = client.post("/productos/", json=payload_invalido)
    assert response.status_code == 422


def test_07_crear_producto_stock_negativo_error():
    # Stock < 0 rompe la regla ge=0 de Pydantic
    payload_invalido = {
        "nombre": "Producto Stock Negativo",
        "precio": 10.0,
        "stock": -5,
    }
    response = client.post("/productos/", json=payload_invalido)
    assert response.status_code == 422


def test_08_obtener_producto_id_inexistente_error():
    response = client.get("/productos/99999999")
    assert response.status_code == 404


def test_09_actualizar_producto_inexistente_error():
    update_payload = {"nombre": "Producto Inexistente", "precio": 50.0}
    response = client.put("/productos/99999999", json=update_payload)
    assert response.status_code == 404


def test_10_eliminar_producto_inexistente_error():
    response = client.delete("/productos/99999999")
    assert response.status_code == 404
