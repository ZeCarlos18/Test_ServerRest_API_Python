import uuid
import requests
import pytest

ENDPOINT = "https://compassuol.serverest.dev/"

def test_login_com_sucesso():
    payload = new_payload()
    criar_usuario(payload)

    login_payload = {
        "email": payload["email"],
        "password": payload["password"],
    }
    response = fazer_login(login_payload)
    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "authorization" in data
    assert data["authorization"].startswith("Bearer ")

    print(response.json())

def test_login_com_senha_errada():
    payload = new_payload()
    criar_usuario(payload)

    login_payload = {
        "email": payload["email"],
        "password": "senhaErrada123",
    }
    response = fazer_login(login_payload)
    assert response.status_code == 401
    data = response.json()

    assert "message" in data
    assert "invál" in data["message"].lower()

    print("Tentando logar com senha errada:")
    print(response.json())

def test_login_com_email_inexistente():
    login_payload = {
        "email": f"naoexiste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password": "123456",
    }
    response = fazer_login(login_payload)
    assert response.status_code == 401
    data = response.json()

    assert "message" in data
    assert "invál" in data["message"].lower()

    print("Tentando logar com email inexistente:")
    print(response.json())

def test_login_com_campos_vazios():
    response = fazer_login({})
    assert response.status_code == 400
    data = response.json()

    assert "email" in data
    assert "password" in data
    assert "obrigat" in data["email"].lower()
    assert "obrigat" in data["password"].lower()

    print("Tentando logar sem informar email e senha:")
    print(response.json())


def fazer_login(payload):
    return requests.post(ENDPOINT + "/login", json=payload)

def criar_usuario(payload):
    return requests.post(ENDPOINT + "/usuarios", json=payload)

def new_payload():
    return {
        "nome" : f"testeDeJose{str(uuid.uuid4().hex[::4])}",
        "email" : f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }
