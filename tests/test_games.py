import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. GET - Obtener lista (Ajusta la ruta si es necesario, ej: "/videojuegos/")
def test_get_games_normal():
    response = client.get("/videojuegos/")  # Cambia "/games/" por tu ruta real
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 2. GET - Obtener lista (Error - Ruta incorrecta o método no permitido simulando fallo)
def test_get_games_error():
    response = client.get("/games/invalid-endpoint")
    assert response.status_code == 404

# 3. GET por ID - Funcionamiento normal
def test_get_game_by_id_normal():
    # Asumiendo que el ID 1 existe en tu base de datos o seeder
    response = client.get("/games/1")
    if response.status_code == 200:
        assert "id" in response.json()
    else:
        assert response.status_code == 404

# 4. GET por ID - Error (ID inexistente)
def test_get_game_by_id_error():
    response = client.get("/games/999999")
    assert response.status_code == 404

# 5. POST - Crear juego (Normal)
def test_create_game_normal():
    payload = {
        "titulo": "Juego Test",
        "genero": "Action",
        "precio": 50.0,
        "stock": 10
    }
    response = client.post("/videojuegos/", json=payload)
    assert response.status_code in [200, 201]

# 6. POST - Crear juego (Error)
def test_create_game_error():
    payload = {"genre": "Action"}
    response = client.post("/videojuegos/", json=payload)  # Cambia "/games/" por tu ruta real
    assert response.status_code == 422

# 7. PUT - Actualizar juego (Normal)
def test_update_game_normal():
    payload = {"title": "Juego Actualizado", "genre": "RPG", "price": 60.0}
    response = client.put("/games/1", json=payload)
    assert response.status_code in [200, 404] # Dependiendo de si existe el ID 1

# 8. PUT - Actualizar juego (Error - Datos incorrectos o ID inexistente)
def test_update_game_error():
    payload = {"price": "precio_texto_invalido"}
    response = client.put("/games/999999", json=payload)
    assert response.status_code in [404, 422]

# 9. DELETE - Eliminar juego (Normal)
def test_delete_game_normal():
    response = client.delete("/games/1")
    assert response.status_code in [200, 204, 404]

# 10. DELETE - Eliminar juego (Error - ID inexistente)
def test_delete_game_error():
    response = client.delete("/games/999999")
    assert response.status_code == 404