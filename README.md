# Testes Automatizados - ServeRest API

## 📋 Descrição

Suite de testes automatizados desenvolvida em **Python + Pytest** para validar todos os cenários do endpoint de **Usuários** da API [ServeRest](https://compassuol.serverest.dev/).

Este projeto faz parte do **Desafio Semana 3** do Bootcamp QA, com objetivo de criar testes de qualidade com validações robustas, dados dinâmicos e independência entre testes.

---

## ✅ Requisitos

- **Python** 3.8 ou superior
- **pip** (gerenciador de pacotes Python)
- Conexão com a internet (para acessar a API)

---

## 🚀 Instalação

### 1. Clonar ou fazer download do repositório

git clone https://github.com/ZeCarlos18/Test_ServerRest_API_Python
cd Test_ServerRest_API_Python

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install pytest requests
```

---

## 📝 Estrutura do Projeto

```
Test_ServerRest_API_Python/
│
├── test_serverRest_api.py      # Arquivo principal com todos os testes
├── README.md                     # Este arquivo
└── requirements.txt              # Dependências do projeto
```

### Executar todos os testes

pytest test_serverRest_api.py -v

**Saída esperada:**

test_listar_usuarios PASSED                                   
test_listar_usuarios_por_nome PASSED                           
test_listar_usuarios_por_email PASSED                         
test_criar_usuario_com_sucesso PASSED                         
test_criar_usuario_com_email_duplicado PASSED              
test_criar_usuario_sem_nome PASSED                             
test_buscar_usuario_por_id PASSED                              
test_buscar_usuario_por_id_invalido PASSED                     
test_excluir_usuario PASSED                                   
test_editar_usuario PASSED                                     


## 📊 Testes Disponíveis

Total: **10 testes**

### 1. `test_listar_usuarios`
**Objetivo:** Validar listagem geral de usuários

**O que testa:**
- Status code 200 (sucesso)
- Estrutura da resposta (`quantidade`, `usuarios`)
- Tipos de dados corretos

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_listar_usuarios -v -s
```

---

### 2. `test_listar_usuarios_por_nome`
**Objetivo:** Listar usuários filtrando por nome

**O que testa:**
- Filtro por nome funcionando
- Usuário criado apareça nos resultados
- Status code 200

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_listar_usuarios_por_nome -v -s
```

---

### 3. `test_listar_usuarios_por_email`
**Objetivo:** Listar usuários filtrando por email

**O que testa:**
- Filtro por email funcionando
- Retorna exatamente 1 resultado com email correto
- Status code 200

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_listar_usuarios_por_email -v -s
```

---

### 4. `test_criar_usuario_com_sucesso`
**Objetivo:** Criar um novo usuário com dados válidos

**O que testa:**
- Status code 201 (criado com sucesso)
- Resposta contém `_id` (ID único gerado)
- Dados retornados correspondem aos enviados
- Todos os campos presentes na resposta

**Dados de exemplo:**
```
{
  "nome": "testeDeJose1a2b3c4d",
  "email": "teste5f6g7h@gmail.com",
  "password": "123456",
  "administrador": "true"
}
```

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_criar_usuario_com_sucesso -v -s
```

---

### 5. `test_criar_usuario_com_email_duplicado`
**Objetivo:** Validar rejeição de email duplicado

**O que testa:**
- Primeiro usuário criado com sucesso (201)
- Tentativa de criar novo usuário com mesmo email retorna 400 (erro)
- Mensagem de erro contém "email"

**Fluxo:**
1. Criar usuário A com email `teste@gmail.com` → 201 ✅
2. Criar usuário B com email `teste@gmail.com` → 400 ❌

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_criar_usuario_com_email_duplicado -v -s
```

---

### 6. `test_criar_usuario_sem_nome`
**Objetivo:** Validar que campo "nome" é obrigatório

**O que testa:**
- Status code 400 (erro de validação)
- Mensagem de erro contém "nome"

**Payload enviado:**
```
{
  "email": "teste1a2b@gmail.com",
  "password": "123456",
  "administrador": "true"
  // ❌ "nome" faltando
}
```

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_criar_usuario_sem_nome -v -s
```

---

### 7. `test_buscar_usuario_por_id`
**Objetivo:** Buscar um usuário específico pelo ID

**O que testa:**
- Status code 200
- ID retornado corresponde ao solicitado
- Todos os dados do usuário são retornados corretamente
- Email e nome coincidem com criação

**Fluxo:**
1. Criar novo usuário
2. Listar usuários
3. Encontrar ID do usuário criado
4. Buscar usuário por ID → validar dados

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_buscar_usuario_por_id -v -s
```

---

### 8. `test_buscar_usuario_por_id_invalido`
**Objetivo:** Validar erro ao buscar ID que não existe

**O que testa:**
- Status code 400 (erro)
- Mensagem de erro existe

**ID testado:** `invalid_id`

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_buscar_usuario_por_id_invalido -v -s
```

---

### 9. `test_excluir_usuario`
**Objetivo:** Excluir um usuário da base de dados

**O que testa:**
- Status code 200 (sucesso)
- Resposta contém mensagem de confirmação
- Usuário realmente foi removido

**Fluxo:**
1. Criar novo usuário
2. Listar usuários
3. Encontrar ID do usuário criado
4. Deletar usuário → 200 

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_excluir_usuario -v -s
```

---

### 10. `test_editar_usuario`
**Objetivo:** Atualizar dados de um usuário existente

**O que testa:**
- Status code 200 (sucesso)
- Dados realmente foram atualizados
- ID permanece o mesmo
- Nome e email foram modificados com sucesso

**Fluxo:**
1. Criar usuário A com nome "jose123"
2. Listar e encontrar ID
3. Editar para nome "jose123 - Atualizado"
4. Validar que nome foi alterado

**Exemplo de execução:**
```bash
pytest test_serverRest_api.py::test_editar_usuario -v -s
```

---

## 🔄 Dados Dinâmicos

Todos os testes usam **UUIDs aleatórios** para evitar conflitos entre execuções:

```python
def new_payload():
    return {
        "nome": f"testeDeJose{str(uuid.uuid4().hex[::4])}",
        "email": f"teste{str(uuid.uuid4().hex[::4])}@gmail.com",
        "password": "123456",
        "administrador": "true",
    }
```
---

## 🛠️ Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'requests'`

**Solução:** Instale as dependências
```bash
pip install requests pytest
```

### Erro: `ConnectionError` ao executar testes

**Possíveis causas:**
- Sem conexão com internet
- API ServeRest fora do ar
- Firewall/proxy bloqueando a conexão

**Solução:** Verifique a conectividade:
```bash
ping compassuol.serverest.dev
```

### Erro: `AssertionError` em um teste

**O que fazer:**
1. Execute novamente com `-v -s` para ver mais detalhes
2. Verifique o status code retornado
3. Verifique a resposta JSON da API
4. Consulte a documentação da ServeRest

**Exemplo:**
```bash
pytest test_serverRest_api.py::test_criar_usuario_com_sucesso -v -s --tb=long
```

---

## 🌐 Referências

- **API ServeRest**: https://compassuol.serverest.dev/

---
