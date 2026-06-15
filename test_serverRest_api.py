import uuid
import requests
import pytest
import jsonschema

ENDPOINT = "https://compassuol.serverest.dev/"

SCHEMA_LISTAR_USUARIOS = {
    "type": "object",
    "required": ["quantidade", "usuarios"],
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nome", "email", "password", "administrador", "_id"],
                "properties": {
                    "nome": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "administrador": {"type": "string"},
                    "_id": {"type": "string"},
                },
            },
        },
    },
}

def test_listar_usuarios():
    response = listar_usuarios()
    assert response.status_code == 200
    data = response.json()
    
    assert "quantidade" in data
    assert "usuarios" in data
    assert isinstance(data["usuarios"], list)
    assert isinstance(data["quantidade"], int)
    
    for usuario in data["usuarios"]:
        print(f"ID: {usuario['_id']}, Nome: {usuario['nome']}, Email: {usuario['email']}")

def test_schema_listar_usuarios():
    response = listar_usuarios()
    assert response.status_code == 200
    data = response.json()

    jsonschema.validate(instance=data, schema=SCHEMA_LISTAR_USUARIOS)
    print("Resposta de GET /usuarios é válida conforme o JSON Schema esperado")

def test_listar_usuarios_por_nome():
    payload = new_payload()
    criar_usuario(payload)

    response = listar_usuarios(nome=payload["nome"])
    assert response.status_code == 200
    data = response.json()
    usuarios = data["usuarios"]
    
    assert len(usuarios) > 0
    assert any(u["nome"] == payload["nome"] for u in usuarios)
    
    print(f"Usuários encontrados com o nome '{payload['nome']}'")
    for usuario in usuarios:
        print(f"ID: {usuario['_id']}, Nome: {usuario['nome']}, Email: {usuario['email']}")

def test_listar_usuarios_por_email():
    payload = new_payload()
    criar_usuario(payload)

    response = listar_usuarios(email=payload["email"])
    assert response.status_code == 200
    data = response.json()
    usuarios = data["usuarios"]
    
    assert len(usuarios) == 1
    assert usuarios[0]["email"] == payload["email"]
    
    print(f"Usuários encontrados com o email '{payload['email']}'")
    for usuario in usuarios:
        print(f"ID: {usuario['_id']}, Nome: {usuario['nome']}, Email: {usuario['email']}")

def test_criar_usuario_com_sucesso():
    payload = new_payload()
    response = criar_usuario(payload)
    assert response.status_code == 201
    data = response.json()

    assert "_id" in data
    assert data["message"] == "Cadastro realizado com sucesso"

    print(response.json())

def test_criar_usuario_com_email_duplicado():
    payload = new_payload()
    usuario_criado = criar_usuario(payload)
    assert usuario_criado.status_code == 201
    print(usuario_criado.json())
    
    print("Tentando criar um novo usuario com o mesmo email:")
    response = criar_usuario(payload)
    assert response.status_code == 400
    data = response.json()
    
    assert "message" in data
    assert "email" in data["message"].lower()
    
    print(response.json())

def test_criar_usuario_sem_nome():
    payload = {
        "email" : f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }
    response = criar_usuario(payload)
    assert response.status_code == 400
    data = response.json()

    assert "nome" in data
    assert data["nome"] == "nome é obrigatório"

    print("Tentando criar um novo usuario sem nome:")
    print(response.json())

def test_buscar_usuario_por_id():
    payload = new_payload()
    criar_usuario(payload)

    listar_response = listar_usuarios()
    usuarios = listar_response.json()["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None

    response = buscar_usuario_por_id(id_usuario)
    assert response.status_code == 200
    data = response.json()
    
    assert data["_id"] == id_usuario
    assert data["email"] == payload["email"]
    assert data["nome"] == payload["nome"]
    assert data["password"] == payload["password"]
    assert "administrador" in data
    
    print(response.json())

def test_buscar_usuario_por_id_formato_invalido():
    response = buscar_usuario_por_id("123456789123456")
    assert response.status_code == 400
    data = response.json()

    assert "id" in data
    assert data["id"] == "id deve ter exatamente 16 caracteres alfanuméricos"

    print(response.json())

def test_buscar_usuario_por_id_nao_encontrado():
    response = buscar_usuario_por_id("1234567891234567")
    assert response.status_code == 400
    data = response.json()

    assert "message" in data
    assert data["message"] == "Usuário não encontrado"

    print(response.json())

def test_excluir_usuario():
    payload = new_payload()
    criar_usuario(payload)

    listar_response = listar_usuarios()
    usuarios = listar_response.json()["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None
    print(f"Usuario criado com sucesso. Excluindo o usuário: {buscar_usuario_por_id(id_usuario).json()}")

    response = excluir_usuario(id_usuario)
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data
    
    print(response.json())

def test_editar_usuario():
    payload = new_payload()
    criar_usuario(payload)

    listar_response = listar_usuarios()
    usuarios = listar_response.json()["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None
    print(f"Usuario criado com sucesso. Dados do usuario: {buscar_usuario_por_id(id_usuario).json()}")

    novo_payload = {
        "nome" : f"testeDeJose{str(uuid.uuid4().hex[::4])} - Atualizado",
        "email" : f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }

    response = editar_usuario(id_usuario, novo_payload)
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Registro alterado com sucesso"

    usuario_atualizado = buscar_usuario_por_id(id_usuario).json()
    assert usuario_atualizado["nome"] == novo_payload["nome"]
    assert usuario_atualizado["email"] == novo_payload["email"]

    print(response.json())
    print(f"Usuario editado com sucesso. Dados atualizados do usuario: {usuario_atualizado}")


def listar_usuarios(nome=None, email=None, _id=None, administrador=None):
    params = {}
    if nome:
        params["nome"] = nome
    if email:
        params["email"] = email
    if _id:
        params["_id"] = _id
    if administrador:
        params["administrador"] = administrador
    return requests.get(ENDPOINT + "/usuarios", params=params)

def criar_usuario(payload):
    return requests.post(ENDPOINT + "/usuarios", json=payload)

def buscar_usuario_por_id(user_id):
    return requests.get(ENDPOINT + f"/usuarios/{user_id}")

def excluir_usuario(user_id):
    return requests.delete(ENDPOINT + f"/usuarios/{user_id}")

def editar_usuario(user_id, payload):
    return requests.put(ENDPOINT + f"/usuarios/{user_id}", json=payload)

def pegar_id_usuario(usuarios, payload):
    for usuario in usuarios:
        if usuario["nome"] == payload["nome"] and usuario["email"] == payload["email"]:
            return usuario["_id"]
    return None    
    
def new_payload():
    return {
        "nome" : f"testeDeJose{str(uuid.uuid4().hex[::4])}",
        "email" : f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }