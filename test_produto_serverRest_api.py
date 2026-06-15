import uuid
import requests
import pytest
import jsonschema

ENDPOINT = "https://compassuol.serverest.dev/"

SCHEMA_LISTAR_PRODUTOS = {
    "type": "object",
    "required": ["quantidade", "produtos"],
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nome", "preco", "descricao", "quantidade", "_id"],
                "properties": {
                    "nome": {"type": "string"},
                    "preco": {"type": "integer"},
                    "descricao": {"type": "string"},
                    "quantidade": {"type": "integer"},
                    "_id": {"type": "string"},
                },
            },
        },
    },
}

def test_listar_produtos():
    response = listar_produtos()
    assert response.status_code == 200
    data = response.json()

    assert "quantidade" in data
    assert "produtos" in data
    assert isinstance(data["produtos"], list)
    assert isinstance(data["quantidade"], int)

    for produto in data["produtos"]:
        print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")

def test_schema_listar_produtos():
    response = listar_produtos()
    assert response.status_code == 200
    data = response.json()

    jsonschema.validate(instance=data, schema=SCHEMA_LISTAR_PRODUTOS)
    print("Resposta de GET /produtos é válida conforme o JSON Schema esperado")

def test_listar_produtos_por_nome():
    token = obter_token_admin()
    payload = new_payload_produto()
    criar_produto(payload, token)

    response = listar_produtos(nome=payload["nome"])
    assert response.status_code == 200
    data = response.json()
    produtos = data["produtos"]

    assert len(produtos) > 0
    assert any(p["nome"] == payload["nome"] for p in produtos)

    print(f"Produtos encontrados com o nome '{payload['nome']}'")
    for produto in produtos:
        print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")

def test_cadastrar_produto_com_sucesso():
    token = obter_token_admin()
    payload = new_payload_produto()

    response = criar_produto(payload, token)
    assert response.status_code == 201
    data = response.json()

    assert "_id" in data
    assert "message" in data

    print(response.json())

def test_cadastrar_produto_com_nome_duplicado():
    token = obter_token_admin()
    payload = new_payload_produto()

    produto_criado = criar_produto(payload, token)
    assert produto_criado.status_code == 201
    print(produto_criado.json())

    print("Tentando cadastrar um novo produto com o mesmo nome:")
    response = criar_produto(payload, token)
    assert response.status_code == 400
    data = response.json()

    assert "message" in data
    assert "nome" in data["message"].lower()

    print(response.json())

def test_cadastrar_produto_sem_token():
    payload = new_payload_produto()

    response = criar_produto(payload)
    assert response.status_code == 401
    data = response.json()

    assert "message" in data

    print("Tentando cadastrar produto sem token:")
    print(response.json())

def test_cadastrar_produto_com_token_nao_admin():
    token = obter_token_nao_admin()
    payload = new_payload_produto()

    response = criar_produto(payload, token)
    assert response.status_code == 403
    data = response.json()

    assert "message" in data
    assert "administradores" in data["message"].lower()

    print("Tentando cadastrar produto com usuário não administrador:")
    print(response.json())

def test_buscar_produto_por_id():
    token = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token)
    id_produto = produto_criado.json()["_id"]

    response = buscar_produto_por_id(id_produto)
    assert response.status_code == 200
    data = response.json()

    assert data["_id"] == id_produto
    assert data["nome"] == payload["nome"]
    assert data["preco"] == payload["preco"]
    assert data["descricao"] == payload["descricao"]
    assert data["quantidade"] == payload["quantidade"]

    print(response.json())

def test_buscar_produto_por_id_invalido():
    id_inexistente = uuid.uuid4().hex[:16]
    response = buscar_produto_por_id(id_inexistente)
    assert response.status_code == 400
    data = response.json()

    assert "message" in data
    assert "não encontrado" in data["message"].lower()

    print(response.json())

def test_editar_produto():
    token = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token)
    id_produto = produto_criado.json()["_id"]
    print(f"Produto criado com sucesso. Dados do produto: {buscar_produto_por_id(id_produto).json()}")

    novo_payload = new_payload_produto()
    novo_payload["preco"] = 999
    novo_payload["quantidade"] = 50

    response = editar_produto(id_produto, novo_payload, token)
    assert response.status_code == 200
    data = response.json()

    assert "message" in data

    print(response.json())
    print(f"Produto editado com sucesso. Dados atualizados: {buscar_produto_por_id(id_produto).json()}")

def test_editar_produto_com_id_inexistente():
    token = obter_token_admin()
    payload = new_payload_produto()
    id_inexistente = uuid.uuid4().hex[:16]

    response = editar_produto(id_inexistente, payload, token)
    assert response.status_code == 201
    data = response.json()

    assert "message" in data
    assert "_id" in data

    print("Editando produto com ID inexistente (deve criar novo registro):")
    print(response.json())

def test_editar_produto_sem_token():
    token = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token)
    id_produto = produto_criado.json()["_id"]

    novo_payload = new_payload_produto()
    response = editar_produto(id_produto, novo_payload)
    assert response.status_code == 401
    data = response.json()

    assert "message" in data

    print("Tentando editar produto sem token:")
    print(response.json())

def test_editar_produto_com_token_nao_admin():
    token_admin = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token_admin)
    id_produto = produto_criado.json()["_id"]

    token_nao_admin = obter_token_nao_admin()
    novo_payload = new_payload_produto()
    response = editar_produto(id_produto, novo_payload, token_nao_admin)
    assert response.status_code == 403
    data = response.json()

    assert "message" in data
    assert "administradores" in data["message"].lower()

    print("Tentando editar produto com usuário não administrador:")
    print(response.json())

def test_excluir_produto():
    token = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token)
    id_produto = produto_criado.json()["_id"]
    print(f"Produto criado com sucesso. Excluindo o produto: {buscar_produto_por_id(id_produto).json()}")

    response = excluir_produto(id_produto, token)
    assert response.status_code == 200
    data = response.json()

    assert "message" in data

    print(response.json())

def test_excluir_produto_sem_token():
    token = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token)
    id_produto = produto_criado.json()["_id"]

    response = excluir_produto(id_produto)
    assert response.status_code == 401
    data = response.json()

    assert "message" in data

    print("Tentando excluir produto sem token:")
    print(response.json())

def test_excluir_produto_com_token_nao_admin():
    token_admin = obter_token_admin()
    payload = new_payload_produto()
    produto_criado = criar_produto(payload, token_admin)
    id_produto = produto_criado.json()["_id"]

    token_nao_admin = obter_token_nao_admin()
    response = excluir_produto(id_produto, token_nao_admin)
    assert response.status_code == 403
    data = response.json()

    assert "message" in data
    assert "administradores" in data["message"].lower()

    print("Tentando excluir produto com usuário não administrador:")
    print(response.json())


def listar_produtos(nome=None, preco=None, descricao=None, quantidade=None, _id=None):
    params = {}
    if nome:
        params["nome"] = nome
    if preco:
        params["preco"] = preco
    if descricao:
        params["descricao"] = descricao
    if quantidade:
        params["quantidade"] = quantidade
    if _id:
        params["_id"] = _id
    return requests.get(ENDPOINT + "/produtos", params=params)

def criar_produto(payload, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.post(ENDPOINT + "/produtos", json=payload, headers=headers)

def buscar_produto_por_id(produto_id):
    return requests.get(ENDPOINT + f"/produtos/{produto_id}")

def editar_produto(produto_id, payload, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.put(ENDPOINT + f"/produtos/{produto_id}", json=payload, headers=headers)

def excluir_produto(produto_id, token=None):
    headers = {"Authorization": token} if token else {}
    return requests.delete(ENDPOINT + f"/produtos/{produto_id}", headers=headers)

def criar_usuario(payload):
    return requests.post(ENDPOINT + "/usuarios", json=payload)

def fazer_login(payload):
    return requests.post(ENDPOINT + "/login", json=payload)

def new_payload_usuario(administrador="true"):
    return {
        "nome" : f"testeDeJose{str(uuid.uuid4().hex[::4])}",
        "email" : f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password" : "123456",
        "administrador" : administrador,
    }

def obter_token_admin():
    payload = new_payload_usuario(administrador="true")
    criar_usuario(payload)
    response = fazer_login({"email": payload["email"], "password": payload["password"]})
    return response.json()["authorization"]

def obter_token_nao_admin():
    payload = new_payload_usuario(administrador="false")
    criar_usuario(payload)
    response = fazer_login({"email": payload["email"], "password": payload["password"]})
    return response.json()["authorization"]

def new_payload_produto():
    return {
        "nome" : f"produtoTesteJose{str(uuid.uuid4().hex[::4])}",
        "preco" : 100,
        "descricao" : "Mouse sem fio",
        "quantidade" : 10,
    }
