# Testes Automatizados - ServeRest API

## 📋 Descrição

Suite de testes automatizados desenvolvida em **Python + Pytest** para validar cenários dos endpoints de **Usuários**, **Login** e **Produtos** da API [ServeRest](https://compassuol.serverest.dev/).

Este projeto começou no **Desafio Semana 3** do Bootcamp QA (testes de **Usuários**) e está sendo evoluído para uma suíte mais completa e profissional, incluindo planejamento de testes, expansão de cobertura (**Login** e **Produtos**), análise de cobertura e reporte de bugs.

📄 O planejamento completo (objetivo, estratégia, escopo, cenários e critérios de qualidade) está em [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md).

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
├── test_serverRest_api.py         # Testes do endpoint de Usuários (Semana 3)
├── test_login_serverRest_api.py   # Testes do endpoint de Login
├── test_produto_serverRest_api.py # Testes do endpoint de Produtos
├── PLANO-DE-TESTES.md             # Plano de testes: objetivo, estratégia, escopo e cenários
├── README.md                     # Este arquivo
└── requirements.txt              # Dependências do projeto
```

> Os arquivos `test_login_serverRest_api.py` e `test_produto_serverRest_api.py` fazem parte da evolução desta suíte e seguem o mesmo padrão (helpers + dados dinâmicos com `uuid`) já usado em `test_serverRest_api.py`. Os cenários estão detalhados no [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md).

### Executar todos os testes

```bash
pytest -v
```

Ou cada suíte individualmente:

```bash
pytest test_serverRest_api.py -v          # Usuários
pytest test_login_serverRest_api.py -v    # Login
pytest test_produto_serverRest_api.py -v  # Produtos
```

**Saída esperada (Usuários):**

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

> ⚠️ Na execução atual contra a API pública, 4 destes testes (`test_criar_usuario_com_sucesso`, `test_criar_usuario_sem_nome`, `test_buscar_usuario_por_id_invalido`, `test_editar_usuario`) falham porque a resposta real da API não segue o schema documentado no Swagger. Ver [🐞 Bugs Encontrados](#-bugs-encontrados).

**Saída esperada (Login e Produtos):** os 19 testes de `test_login_serverRest_api.py` e `test_produto_serverRest_api.py` passam 100% (`pytest test_login_serverRest_api.py test_produto_serverRest_api.py -v`).


## 📊 Testes Disponíveis

A suíte soma **29 testes** divididos em 3 arquivos: **Usuários** (10), **Login** (4) e **Produtos** (15).

### Usuários — `test_serverRest_api.py` (10 testes)

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

### Login — `test_login_serverRest_api.py` (4 testes)

| Teste | Objetivo | Resultado esperado |
|---|---|---|
| `test_login_com_sucesso` | Login com e-mail/senha de um usuário recém-cadastrado | 200, resposta com `message` e `authorization` (`Bearer <token>`) |
| `test_login_com_senha_errada` | Login com senha incorreta para um usuário existente | 401, `message` = "Email e/ou senha inválidos" |
| `test_login_com_email_inexistente` | Login com e-mail que não existe na base | 401, `message` = "Email e/ou senha inválidos" |
| `test_login_com_campos_vazios` | Login sem informar `email`/`password` | 400, resposta com `email` e `password` indicando campo obrigatório |

**Exemplo de execução:**
```bash
pytest test_login_serverRest_api.py -v -s
```

---

### Produtos — `test_produto_serverRest_api.py` (15 testes)

| Teste | Objetivo | Resultado esperado |
|---|---|---|
| `test_listar_produtos` | Listar todos os produtos cadastrados | 200, estrutura `{quantidade, produtos[]}` |
| `test_listar_produtos_por_nome` | Filtrar produtos pelo parâmetro `nome` | 200, produto criado aparece no resultado |
| `test_cadastrar_produto_com_sucesso` | Cadastrar produto com token de usuário administrador | 201, resposta com `message` e `_id` |
| `test_cadastrar_produto_com_nome_duplicado` | Cadastrar produto com nome já existente | 400, `message` contém "nome" |
| `test_cadastrar_produto_sem_token` | Cadastrar produto sem header `Authorization` | 401, mensagem de token ausente/inválido |
| `test_cadastrar_produto_com_token_nao_admin` | Cadastrar produto com token de usuário não administrador | 403, `message` = "Rota exclusiva para administradores" |
| `test_buscar_produto_por_id` | Buscar produto pelo `_id` retornado no cadastro | 200, dados do produto coincidem com o payload enviado |
| `test_buscar_produto_por_id_invalido` | Buscar produto com `_id` no formato válido, porém inexistente | 400, `message` = "Produto não encontrado" |
| `test_editar_produto` | Editar produto existente com token de admin | 200, `message` = "Registro alterado com sucesso" |
| `test_editar_produto_com_id_inexistente` | Editar (PUT) um `_id` que não existe | 201, cria novo registro (`message` + `_id`) |
| `test_editar_produto_sem_token` | Editar produto sem header `Authorization` | 401, mensagem de token ausente/inválido |
| `test_editar_produto_com_token_nao_admin` | Editar produto com token de usuário não administrador | 403, `message` = "Rota exclusiva para administradores" |
| `test_excluir_produto` | Excluir produto existente com token de admin | 200, mensagem de confirmação |
| `test_excluir_produto_sem_token` | Excluir produto sem header `Authorization` | 401, mensagem de token ausente/inválido |
| `test_excluir_produto_com_token_nao_admin` | Excluir produto com token de usuário não administrador | 403, `message` = "Rota exclusiva para administradores" |

> Os testes que exigem privilégio de administrador criam um usuário (`administrador: "true"` ou `"false"`) e fazem login em `/login` para obter o token usado no header `Authorization`.

**Exemplo de execução:**
```bash
pytest test_produto_serverRest_api.py -v -s
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

## 📊 Cobertura de Testes

A cobertura desta suíte é calculada com base nas métricas descritas no artigo [*Como verificar a cobertura de testes da API REST*](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b), aplicando-as ao inventário de endpoints da [API ServeRest](https://compassuol.serverest.dev/) (recursos **Login**, **Usuários**, **Produtos** e **Carrinhos**).

### Método usado

| Métrica | Fórmula |
|---|---|
| **Path Coverage** | nº de *paths* (endpoints) com pelo menos 1 teste ÷ nº total de *paths* da API |
| **Operator Coverage** | nº de operações (método HTTP + path) testadas ÷ nº total de operações da API |
| **Status Code Coverage** | nº de status codes distintos validados pelos testes ÷ nº de status codes documentados para os endpoints em escopo (Login, Usuários, Produtos) |

**Inventário total da API** (referência para os cálculos): 9 *paths* e 16 operações (método + path), distribuídos em `/login`, `/usuarios`, `/usuarios/{_id}`, `/produtos`, `/produtos/{_id}`, `/carrinhos`, `/carrinhos/{_id}`, `/carrinhos/concluir-compra` e `/carrinhos/cancelar-compra`.

### Cobertura atual (Usuários + Login + Produtos)

| Métrica | Cálculo | Resultado |
|---|---|---|
| Path Coverage | 5 paths testados (`/usuarios`, `/usuarios/{_id}`, `/login`, `/produtos`, `/produtos/{_id}`) ÷ 9 paths totais | **≈ 56%** |
| Operator Coverage | 11 operações testadas (5 de Usuários + 1 de Login + 5 de Produtos) ÷ 16 operações totais | **≈ 69%** |
| Status Code Coverage | 5 status codes testados (200, 201, 400, 401, 403) ÷ 5 status codes relevantes ao escopo | **100%** |

A suíte agora soma **29 testes** em 3 arquivos: `test_serverRest_api.py` (Usuários, 10 testes), `test_login_serverRest_api.py` (Login, 4 testes) e `test_produto_serverRest_api.py` (Produtos, 15 testes). Os 19 testes novos (Login + Produtos) passam 100%; os detalhes sobre falhas pré-existentes na suíte de Usuários estão na seção [🐞 Bugs Encontrados](#-bugs-encontrados).

### Cenários que ficaram fora (e por quê)

- **Endpoint `/carrinhos`** (3 *paths*, 5 operações): não foi solicitado neste desafio. É o principal responsável pela diferença entre 56%/69% e 100% de Path/Operator Coverage — incluí-lo elevaria a cobertura total, mas está fora do escopo definido em [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md).
- **Expiração do token de login (600s)**: testar o cenário real de expiração exigiria aguardar 10 minutos por execução (ou manipular o relógio do servidor), o que é inviável para a suíte de regressão. O comportamento de token *ausente/inválido* (401/403) é coberto via Produtos.
- **Status codes de erro de servidor (5xx)**: não são documentados oficialmente por operação e dependem de falhas internas não reproduzíveis sob demanda; portanto não fazem parte do denominador de Status Code Coverage.
- **Testes de carga, concorrência e segurança aprofundada (fuzzing, SQL injection, etc.)**: fora do objetivo funcional desta suíte (ver seção *Fora de escopo* do [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md)).

---

## 🐞 Bugs Encontrados

Bugs identificados durante a execução da suíte são reportados na aba [Issues](../../issues) deste repositório, seguindo o padrão: **Passos para reproduzir**, **Resultado esperado**, **Resultado obtido**, **Severidade** e **Evidências** (logs/prints da resposta da API).

### Bug candidato: respostas de erro/sucesso não seguem o schema documentado no Swagger

Ao rodar `test_serverRest_api.py` (suíte de Usuários) contra a API pública, **4 dos 10 testes falham** porque a resposta real da API diverge do schema documentado:

| Operação | Schema documentado | Resposta real obtida |
|---|---|---|
| `POST /usuarios` (sucesso) | `{ "_id", "nome", "email", "password", "administrador" }` | `{ "message": "Cadastro realizado com sucesso", "_id": "..." }` — não ecoa `nome`/`email`/`password`/`administrador` |
| `POST /usuarios` sem `nome` | `{ "message": "..." }` | `{ "nome": "nome é obrigatório" }` — chave é o nome do campo, não `message` |
| `GET /usuarios/{_id}` com id em formato inválido | `{ "message": "Usuário não encontrado" }` | `{ "id": "id deve ter exatamente 16 caracteres alfanuméricos" }` — chave é `id`, não `message` |
| `PUT /usuarios/{_id}` (sucesso) | retorna os dados atualizados (`nome`, `email`, `_id`, ...) | `{ "message": "Registro alterado com sucesso" }` — não ecoa os dados atualizados |

O mesmo padrão (erros de validação retornando `{<campo>: "<campo> é obrigatório"}` em vez de `{message: ...}`, e id mal formatado retornando `{id: "id deve ter exatamente 16 caracteres alfanuméricos"}`) também ocorre em `/login` e `/produtos`, mas nesses casos os testes em `test_login_serverRest_api.py` e `test_produto_serverRest_api.py` já foram escritos validando o comportamento real (por isso passam 100%).

- **Severidade sugerida:** Baixa/Média — não impede o uso da API, mas o schema documentado no Swagger não corresponde ao retorno real, o que quebra integrações/testes escritos a partir da documentação.
- **Evidências:** rodar `pytest test_serverRest_api.py -v -s` reproduz as 4 falhas com os corpos de resposta reais impressos no console.

> Próximo passo: abrir uma Issue no GitHub com esse relato (passos para reproduzir, esperado vs. obtido, severidade e print da execução do pytest) e linkar aqui.

---

## 🌐 Referências

- **API ServeRest**: https://compassuol.serverest.dev/
- **Plano de testes**: [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md)
- **Metodologia de cobertura**: [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b)

---
