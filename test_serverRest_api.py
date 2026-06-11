import requests

ENDPOINT = "https://compassuol.serverest.dev/"

def test_logar_usuario():
    payload = new_payload()

    criar_usuario_resposta = criar_usuario(payload)
    print(descobrir_status_code(criar_usuario_resposta.status_code))

    login = {"email": payload["email"], "password": payload["password"]}
    response = logar_usuario(login)
    assert response.status_code == 200

def test_listar_usuarios():
    payload = new_payload()

    criar_usuario_resposta = criar_usuario(payload)
    print(descobrir_status_code(criar_usuario_resposta.status_code))

    response = listar_usuarios()
    data = response.json()
    assert response.status_code == 200
    usuarios = data["usuarios"]
    for usuario in usuarios:
        if usuario["nome"] == payload["nome"] and usuario["email"] == payload["email"]:
            print(data["usuarios"][usuarios.index(usuario)])

def test_criar_usuario():
    payload = new_payload()
    response = criar_usuario(payload)
    assert response.status_code == 201 or response.status_code == 400    
    if response.status_code == 201 or response.status_code == 400:
        print(response.json())

def test_buscar_usuario_por_id():
    payload = new_payload()

    criar_usuario_resposta = criar_usuario(payload)
    print(descobrir_status_code(criar_usuario_resposta.status_code))

    listar_response = listar_usuarios()
    data = listar_response.json()
    usuarios = data["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None

    response = buscar_usuario_por_id(id_usuario)
    assert response.status_code == 200
    print(response.json())

def test_excluir_usuario():
    payload = new_payload()

    criar_usuario_resposta = criar_usuario(payload)
    print(descobrir_status_code(criar_usuario_resposta.status_code))

    listar_response = listar_usuarios()
    data = listar_response.json()
    usuarios = data["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None

    excluir_response = excluir_usuario(id_usuario)
    assert excluir_response.status_code == 200
    print(excluir_response.json())

def test_editar_usuario():
    payload = new_payload()

    criar_usuario_resposta = criar_usuario(payload)
    print(descobrir_status_code(criar_usuario_resposta.status_code))

    listar_response = listar_usuarios()
    data = listar_response.json()
    usuarios = data["usuarios"]
    id_usuario = pegar_id_usuario(usuarios, payload)
    assert id_usuario is not None

    novo_payload = {
        "nome" : "teste_2026-06-11 - Atualizado",
        "email" : "teste_2026-06-11@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }

    response = editar_usuario(id_usuario, novo_payload)
    assert response.status_code == 200
    print(response.json())



def logar_usuario(payload):
    return requests.post(ENDPOINT + "/login", json=payload)

def listar_usuarios():
    return requests.get(ENDPOINT + "/usuarios")

def criar_usuario(payload):
    return requests.post(ENDPOINT + "/usuarios", json=payload)

def buscar_usuario_por_id(user_id):
    return requests.get(ENDPOINT + f"/usuarios/{user_id}")

def excluir_usuario(user_id):
    return requests.delete(ENDPOINT + f"/usuarios/{user_id}")

def editar_usuario(user_id, payload):
    return requests.put(ENDPOINT + f"/usuarios/{user_id}", json=payload)

def descobrir_status_code(status_code):
    if status_code == 200:
        return "Ok"
    elif status_code == 201:
        return "Usuario Criado"
    elif status_code == 400:
        return "Usuario já existe"
    elif status_code == 404:
        return "Não encontrado"
    
def pegar_id_usuario(usuarios, payload):
    for usuario in usuarios:
        if usuario["nome"] == payload["nome"] and usuario["email"] == payload["email"]:
            return usuario["_id"]
    return None    
    
def new_payload():
    return {
        "nome" : "teste_2026-06-11",
        "email" : "teste_2026-06-11@gmail.com",
        "password" : "123456",
        "administrador" : "true",
    }