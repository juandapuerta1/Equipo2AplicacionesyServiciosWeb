"""Pruebas de la API de Mascotas (Juan David Gonzalez Vasco)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

RUTA = "/mascotas/"
ID_INEXISTENTE = 99999999


def _payload(**cambios):
    datos = {
        "nombre": "Test Firulais",
        "especie": "Perro",
        "raza": "Criollo",
        "edad": 3,
        "peso": 12.5,
        "vacunado": True,
    }
    datos.update(cambios)
    return datos


@pytest.fixture(name="mascota_creada")
def _mascota_creada():
    """Crea una mascota para la prueba y la borra al terminar."""
    respuesta = client.post(RUTA, json=_payload())
    assert respuesta.status_code == 201
    mascota = respuesta.json()
    yield mascota
    client.delete(f"{RUTA}{mascota['id']}")


# ==========================================
# GET - Obtener lista
# ==========================================


def test_get_lista_mascotas_normal(mascota_creada):
    respuesta = client.get(RUTA)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert isinstance(cuerpo, list)
    assert mascota_creada["id"] in [m["id"] for m in cuerpo]


def test_get_lista_mascotas_metodo_no_permitido_error():
    # La coleccion solo admite GET y POST: PATCH debe responder 405.
    respuesta = client.patch(RUTA, json={})

    assert respuesta.status_code == 405
    assert respuesta.json() == {"detail": "Method Not Allowed"}
    assert "allow" in respuesta.headers


# ==========================================
# GET - Obtener un registro por ID
# ==========================================


def test_get_mascota_por_id_normal(mascota_creada):
    respuesta = client.get(f"{RUTA}{mascota_creada['id']}")

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["id"] == mascota_creada["id"]
    assert cuerpo["nombre"] == "Test Firulais"
    assert cuerpo["especie"] == "Perro"


def test_get_mascota_por_id_inexistente_error():
    respuesta = client.get(f"{RUTA}{ID_INEXISTENTE}")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Mascota no encontrada"}


# ==========================================
# POST - Crear
# ==========================================


def test_post_crear_mascota_normal():
    datos = _payload(nombre="Test Michi", especie="Gato", raza=None, peso=4.2)

    respuesta = client.post(RUTA, json=datos)

    try:
        assert respuesta.status_code == 201
        cuerpo = respuesta.json()
        assert isinstance(cuerpo["id"], int)
        assert cuerpo["nombre"] == "Test Michi"
        assert cuerpo["especie"] == "Gato"
        assert cuerpo["peso"] == 4.2
        assert cuerpo["vacunado"] is True
    finally:
        if respuesta.status_code == 201:
            client.delete(f"{RUTA}{respuesta.json()['id']}")


def test_post_crear_mascota_datos_invalidos_error():
    # nombre de 1 letra (min_length=2) y edad fuera de rango (max 40)
    respuesta = client.post(RUTA, json=_payload(nombre="A", edad=99))

    assert respuesta.status_code == 422
    campos_con_error = {error["loc"][-1] for error in respuesta.json()["detail"]}
    assert {"nombre", "edad"} <= campos_con_error


# ==========================================
# PUT - Actualizar
# ==========================================


def test_put_actualizar_mascota_normal(mascota_creada):
    cambios = {"nombre": "Test Rocky", "edad": 5, "vacunado": False}

    respuesta = client.put(f"{RUTA}{mascota_creada['id']}", json=cambios)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["id"] == mascota_creada["id"]
    assert cuerpo["nombre"] == "Test Rocky"
    assert cuerpo["edad"] == 5
    assert cuerpo["vacunado"] is False
    # Lo que no se envio se conserva
    assert cuerpo["especie"] == "Perro"


def test_put_actualizar_mascota_inexistente_error():
    respuesta = client.put(f"{RUTA}{ID_INEXISTENTE}", json={"nombre": "Fantasma"})

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Mascota no encontrada"}


# ==========================================
# DELETE - Eliminar
# ==========================================


def test_delete_mascota_normal():
    creada = client.post(RUTA, json=_payload(nombre="Test Borrar"))
    assert creada.status_code == 201
    mascota_id = creada.json()["id"]

    respuesta = client.delete(f"{RUTA}{mascota_id}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    # Ya no debe existir
    assert client.get(f"{RUTA}{mascota_id}").status_code == 404


def test_delete_mascota_inexistente_error():
    respuesta = client.delete(f"{RUTA}{ID_INEXISTENTE}")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Mascota no encontrada"}
