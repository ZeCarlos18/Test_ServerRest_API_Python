# Plano de Testes — ServeRest API

> Documento de planejamento da evolução da suíte criada na Semana 3 (testes do endpoint **Usuários**) para uma suíte mais completa, cobrindo também **Login** e **Produtos**, com análise de cobertura e reporte de bugs.
>
> Este documento é escrito **antes** da evolução do código e é **atualizado conforme o desafio avança**.

---

## 1. Objetivo

Garantir, por meio de testes automatizados de API (Python + Pytest + Requests), que os principais fluxos da [ServeRest API](https://compassuol.serverest.dev/) — **Usuários**, **Login** e **Produtos** — funcionam conforme especificado, incluindo:

- Cenários de sucesso (caminho feliz);
- Cenários de erro/validação (dados inválidos, ausentes ou duplicados);
- Regras de autorização (rotas exclusivas para administradores);
- Estrutura e tipos dos dados retornados pela API.

A suíte deve servir como base de regressão, podendo ser executada localmente e (na versão com o Extra 2) automaticamente via CI a cada push.

---

## 2. Estratégia

| Item | Definição |
|---|---|
| **Tipo de teste** | Testes funcionais de API, caixa-preta (black-box), via chamadas HTTP diretas |
| **Camada** | Testes de integração contra o ambiente público da ServeRest (`https://compassuol.serverest.dev/`) — não há acesso ao código-fonte da API |
| **Ferramentas** | Python 3, `pytest` (execução/asserts), `requests` (cliente HTTP), `uuid` (geração de dados únicos), `jsonschema` (Extra 1 — validação de schema), GitHub Actions (Extra 2 — CI) |
| **Organização** | Um arquivo por recurso, mantendo o padrão já usado na Semana 3 (funções auxiliares no fim do arquivo + `new_payload()` para dados dinâmicos): `test_serverRest_api.py` (Usuários), `test_login_serverRest_api.py` (Login), `test_produto_serverRest_api.py` (Produtos) |
| **Independência** | Cada teste cria/usa seus próprios dados via `uuid`, não depende de estado deixado por outros testes nem de ordem de execução |
| **Massa de dados** | Para os testes de Produtos que exigem permissão de administrador, um usuário com `administrador: "true"` é criado dinamicamente e autenticado via `/login` para obter o token `Bearer` usado no header `Authorization` |
| **Execução** | `pytest -v` (e `-v -s` para ver os prints de depuração já usados na Semana 3) |

---

## 3. Escopo

### 3.1. Em escopo

- **Usuários** (`/usuarios`, `/usuarios/{_id}`) — já implementado na Semana 3, mantido sem reescrita
- **Login** (`/login`): credenciais corretas, senha errada, e-mail inexistente, campos vazios
- **Produtos** (`/produtos`, `/produtos/{_id}`): listar, cadastrar (com e sem token de admin), buscar por ID, atualizar, excluir
- Validação de **status code** e de **corpo da resposta** (mensagens, campos, tipos)
- Cálculo de cobertura da suíte com base no artigo de referência (ver seção 6)
- Reporte de pelo menos 1 bug encontrado durante a execução, na aba *Issues* do GitHub
- **Extra 1** (✅ implementado): validação de estrutura de resposta via JSON Schema em 3 endpoints — `GET /usuarios` (`test_schema_listar_usuarios`), `POST /login` (`test_schema_login_com_sucesso`) e `GET /produtos` (`test_schema_listar_produtos`)
- **Extra 2**: pipeline de GitHub Actions executando a suíte a cada push

### 3.2. Fora de escopo

- **Carrinho** (`/carrinhos` e rotas relacionadas) — não solicitado neste desafio
- Testes de **performance/carga** (volume de requisições, tempo de resposta sob estresse)
- Testes de **segurança aprofundada** (fuzzing, SQL injection, etc.) além do que surgir naturalmente da validação de entradas
- Testes de **concorrência** (execução paralela / condições de corrida)
- Testes de **expiração de token** (os 600s de validade do token de login não serão testados via espera real, por inviabilidade de tempo de execução)
- Testes de **interface (UI)** — a suíte é 100% via API

---

## 4. Cenários a implementar (por endpoint)

### 4.1. Usuários — `test_serverRest_api.py` (Status: ✅ implementado — 11 testes)

| # | Cenário | Teste | Resultado esperado |
|---|---|---|---|
| 1 | Listar todos os usuários | `test_listar_usuarios` | 200, estrutura `{quantidade, usuarios[]}` |
| 2 | Listar usuários filtrando por nome | `test_listar_usuarios_por_nome` | 200, resultado contém usuário criado |
| 3 | Listar usuários filtrando por e-mail | `test_listar_usuarios_por_email` | 200, exatamente 1 resultado |
| 4 | Cadastrar usuário com dados válidos | `test_criar_usuario_com_sucesso` | 201, retorna `_id` e dados enviados |
| 5 | Cadastrar usuário com e-mail duplicado | `test_criar_usuario_com_email_duplicado` | 400, mensagem menciona "email" |
| 6 | Cadastrar usuário sem o campo `nome` | `test_criar_usuario_sem_nome` | 400, mensagem menciona "nome" |
| 7 | Buscar usuário por ID válido | `test_buscar_usuario_por_id` | 200, dados completos do usuário |
| 8 | Buscar usuário por ID inválido | `test_buscar_usuario_por_id_invalido` | 400, mensagem de erro |
| 9 | Excluir usuário existente | `test_excluir_usuario` | 200, mensagem de confirmação |
| 10 | Editar usuário existente | `test_editar_usuario` | 200, dados atualizados refletidos |
| 11 | (Extra 1) Validar schema de `GET /usuarios` | `test_schema_listar_usuarios` | 200, resposta valida contra `SCHEMA_LISTAR_USUARIOS` |

### 4.2. Login — `test_login_serverRest_api.py` (Status: ✅ implementado — 5 testes)

| # | Cenário | Teste | Resultado esperado |
|---|---|---|---|
| 1 | Login com credenciais corretas (usuário cadastrado previamente) | `test_login_com_sucesso` | 200, resposta contém `message` e `authorization` (`Bearer <token>`) |
| 2 | (Extra 1) Validar schema da resposta de sucesso | `test_schema_login_com_sucesso` | 200, resposta valida contra `SCHEMA_LOGIN_COM_SUCESSO` |
| 3 | Login com senha errada | `test_login_com_senha_errada` | 401, mensagem "Email e/ou senha inválidos" |
| 4 | Login com e-mail inexistente | `test_login_com_email_inexistente` | 401, mensagem "Email e/ou senha inválidos" |
| 5 | Login com campos vazios/ausentes (`email`/`password`) | `test_login_com_campos_vazios` | 400, mensagem indicando campo obrigatório |

> O token obtido no cenário 1 também é reaproveitado como pré-condição (setup) dos testes de Produtos que exigem usuário administrador.

### 4.3. Produtos — `test_produto_serverRest_api.py` (Status: ✅ implementado — 16 testes)

| # | Cenário | Teste | Resultado esperado |
|---|---|---|---|
| 1 | Listar produtos cadastrados | `test_listar_produtos` | 200, estrutura `{quantidade, produtos[]}` |
| 2 | (Extra 1) Validar schema de `GET /produtos` | `test_schema_listar_produtos` | 200, resposta valida contra `SCHEMA_LISTAR_PRODUTOS` |
| 3 | Listar produtos com filtro (ex: por `nome`) | `test_listar_produtos_por_nome` | 200, resultado coerente com filtro |
| 4 | Cadastrar produto com token de usuário **administrador** e nome único | `test_cadastrar_produto_com_sucesso` | 201, retorna `message` e `_id` |
| 5 | Cadastrar produto com nome já existente | `test_cadastrar_produto_com_nome_duplicado` | 400, mensagem "Já existe produto com esse nome" |
| 6 | Cadastrar produto **sem token** | `test_cadastrar_produto_sem_token` | 401, mensagem de token ausente/inválido |
| 7 | Cadastrar produto com token de usuário **não administrador** | `test_cadastrar_produto_com_token_nao_admin` | 403, mensagem "Rota exclusiva para administradores" |
| 8 | Buscar produto por ID válido | `test_buscar_produto_por_id` | 200, dados do produto retornados |
| 9 | Buscar produto por ID em formato válido, porém inexistente | `test_buscar_produto_por_id_invalido` | 400, mensagem "Produto não encontrado" |
| 10 | Atualizar (editar) produto existente com token de admin | `test_editar_produto` | 200, mensagem "Registro alterado com sucesso" |
| 11 | Atualizar produto com ID inexistente (cria novo registro) | `test_editar_produto_com_id_inexistente` | 201, mensagem de cadastro realizado |
| 12 | Atualizar produto sem token | `test_editar_produto_sem_token` | 401, mensagem de token ausente/inválido |
| 13 | Atualizar produto com token de usuário não administrador | `test_editar_produto_com_token_nao_admin` | 403, mensagem "Rota exclusiva para administradores" |
| 14 | Excluir produto existente com token de admin | `test_excluir_produto` | 200, mensagem de exclusão |
| 15 | Excluir produto sem token | `test_excluir_produto_sem_token` | 401, mensagem de token ausente/inválido |
| 16 | Excluir produto com token de usuário não administrador | `test_excluir_produto_com_token_nao_admin` | 403, mensagem "Rota exclusiva para administradores" |

> Fluxo de autenticação: para os cenários 4, 10 e 14 (operações que exigem admin), o teste cria um usuário com `administrador: "true"`, faz login em `/login` e usa o `authorization` retornado no header `Authorization` da requisição. Para os cenários 7, 13 e 16, é usado um usuário com `administrador: "false"`.

### 4.4. Extra 1 — Validação de JSON Schema

Os 3 testes marcados como "(Extra 1)" acima validam a **estrutura completa da resposta** (tipos de dados e campos obrigatórios) usando [`jsonschema`](https://pypi.org/project/jsonschema/):

| Endpoint | Teste | Schema valida |
|---|---|---|
| `GET /usuarios` | `test_schema_listar_usuarios` | `quantidade` (integer) e `usuarios[]` (objetos com `nome`, `email`, `password`, `administrador`, `_id` string) |
| `POST /login` (sucesso) | `test_schema_login_com_sucesso` | `message` e `authorization` (strings obrigatórias) |
| `GET /produtos` | `test_schema_listar_produtos` | `quantidade` (integer) e `produtos[]` (objetos com `nome`/`descricao` string, `preco`/`quantidade` integer, `_id` string) |

Cada schema é um dicionário Python no início do respectivo arquivo de teste, validado com `jsonschema.validate(instance=data, schema=SCHEMA)`. Em caso de divergência (campo ausente/tipo incorreto), o teste falha com `jsonschema.exceptions.ValidationError`.

---

## 5. Critérios de qualidade

Um teste é considerado **pronto** quando:

1. **Independente** — não depende de execuções anteriores, de ordem de execução nem deixa "lixo" que afete outros testes (usa `uuid` para dados únicos);
2. **Determinístico** — produz o mesmo resultado em execuções repetidas, dado o mesmo ambiente;
3. **Valida status code E corpo da resposta** — não basta verificar `status_code`; os campos relevantes da resposta (mensagens, tipos, IDs, valores) também são verificados;
4. **Nome descritivo** — segue o padrão `test_<ação>_<cenário>` (ex.: `test_login_com_senha_errada`), permitindo entender o que é testado sem ler o corpo;
5. **Cobre caminho feliz e cenários de erro** — para cada endpoint relevante, há ao menos um teste de sucesso e um de falha/validação;
6. **Sem credenciais fixas sensíveis** — usuários administradores usados nos testes são criados dinamicamente, não fixos em produção;
7. **Passa de forma consistente** (`pytest -v` 100% verde) no ambiente público da ServeRest, considerando a instabilidade esperada de um ambiente compartilhado;
8. **Documentado** — cada novo arquivo de teste é referenciado no `README.md`, e cenários novos são adicionados a este plano.

---

## 6. Cobertura de testes

A cobertura da suíte é calculada com base nas dimensões propostas no artigo [*Como verificar a cobertura de testes da API REST*](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b), aplicadas ao inventário de endpoints da [API ServeRest](https://compassuol.serverest.dev/) (recursos **Login**, **Usuários**, **Produtos** e **Carrinhos**).

### 6.1. Método usado

| Métrica | Fórmula |
|---|---|
| **Path Coverage** | nº de *paths* (endpoints) com pelo menos 1 teste ÷ nº total de *paths* da API |
| **Operator Coverage** | nº de operações (método HTTP + path) testadas ÷ nº total de operações da API |
| **Status Code Coverage** | nº de status codes distintos validados pelos testes ÷ nº de status codes documentados para os endpoints em escopo (Login, Usuários, Produtos) |

> Outras dimensões citadas no artigo (Parameter Coverage, Parameter Value Coverage, Content-Type Coverage, Operation Flow Coverage, Response Properties Body Coverage) não foram aplicadas isoladamente — a validação de propriedades do corpo da resposta é coberta de forma complementar pelos testes de **JSON Schema** (Extra 1, seção 4.4).

**Inventário total da API** (referência para os cálculos): 9 *paths* e 16 operações (método + path), distribuídos em `/login`, `/usuarios`, `/usuarios/{_id}`, `/produtos`, `/produtos/{_id}`, `/carrinhos`, `/carrinhos/{_id}`, `/carrinhos/concluir-compra` e `/carrinhos/cancelar-compra`.

### 6.2. Cobertura atual (Usuários + Login + Produtos)

| Métrica | Cálculo | Resultado |
|---|---|---|
| Path Coverage | 5 paths testados (`/usuarios`, `/usuarios/{_id}`, `/login`, `/produtos`, `/produtos/{_id}`) ÷ 9 paths totais | **≈ 56%** |
| Operator Coverage | 11 operações testadas (5 de Usuários + 1 de Login + 5 de Produtos) ÷ 16 operações totais | **≈ 69%** |
| Status Code Coverage | 5 status codes testados (200, 201, 400, 401, 403) ÷ 5 status codes relevantes ao escopo | **100%** |

A suíte soma **32 testes** em 3 arquivos: `test_serverRest_api.py` (Usuários, 11 testes), `test_login_serverRest_api.py` (Login, 5 testes) e `test_produto_serverRest_api.py` (Produtos, 16 testes) — incluindo os 3 testes de JSON Schema do Extra 1. Os 22 testes novos (Login + Produtos + Extra 1) passam 100%; os 4 testes de Usuários que falham são causados pelo bug descrito na seção 7.

### 6.3. Cenários que ficaram fora (e por quê)

- **Endpoint `/carrinhos`** (3 *paths*, 5 operações): não foi solicitado neste desafio. É o principal responsável pela diferença entre 56%/69% e 100% de Path/Operator Coverage — incluí-lo elevaria a cobertura total, mas está fora do escopo definido na seção 3.2.
- **Expiração do token de login (600s)**: testar o cenário real de expiração exigiria aguardar 10 minutos por execução (ou manipular o relógio do servidor), o que é inviável para a suíte de regressão. O comportamento de token *ausente/inválido* (401/403) é coberto via Produtos.
- **Status codes de erro de servidor (5xx)**: não são documentados oficialmente por operação e dependem de falhas internas não reproduzíveis sob demanda; portanto não fazem parte do denominador de Status Code Coverage.
- **Testes de carga, concorrência e segurança aprofundada (fuzzing, SQL injection, etc.)**: fora do objetivo funcional desta suíte (ver seção 3.2).

---

## 7. Bug encontrado: respostas de erro/sucesso não seguem o schema documentado no Swagger

Ao rodar `test_serverRest_api.py` (suíte de Usuários) contra a API pública, **4 dos 11 testes falham** porque a resposta real da API diverge do schema documentado no Swagger:

| Operação | Schema documentado | Resposta real obtida |
|---|---|---|
| `POST /usuarios` (sucesso) | `{ "_id", "nome", "email", "password", "administrador" }` | `{ "message": "Cadastro realizado com sucesso", "_id": "..." }` — não ecoa `nome`/`email`/`password`/`administrador` |
| `POST /usuarios` sem `nome` | `{ "message": "..." }` | `{ "nome": "nome é obrigatório" }` — chave é o nome do campo, não `message` |
| `GET /usuarios/{_id}` com id em formato inválido | `{ "message": "Usuário não encontrado" }` | `{ "id": "id deve ter exatamente 16 caracteres alfanuméricos" }` — chave é `id`, não `message` |
| `PUT /usuarios/{_id}` (sucesso) | retorna os dados atualizados (`nome`, `email`, `_id`, ...) | `{ "message": "Registro alterado com sucesso" }` — não ecoa os dados atualizados |

O mesmo padrão (erros de validação retornando `{<campo>: "<campo> é obrigatório"}` em vez de `{message: ...}`, e id mal formatado retornando `{id: "id deve ter exatamente 16 caracteres alfanuméricos"}`) também ocorre em `/login` e `/produtos`, mas nesses casos os testes em `test_login_serverRest_api.py` e `test_produto_serverRest_api.py` já foram escritos validando o comportamento real (por isso passam 100%).

- **Testes afetados:** `test_criar_usuario_com_sucesso`, `test_criar_usuario_sem_nome`, `test_buscar_usuario_por_id_invalido`, `test_editar_usuario`
- **Severidade sugerida:** Baixa/Média — não impede o uso da API, mas o schema documentado no Swagger não corresponde ao retorno real, o que quebra integrações/testes escritos a partir da documentação.
- **Evidências:** rodar `pytest test_serverRest_api.py -v -s` reproduz as 4 falhas com os corpos de resposta reais impressos no console.
- **Status:** reportado na aba [Issues](../../issues) deste repositório, seguindo o padrão Passos para reproduzir / Resultado esperado / Resultado obtido / Severidade / Evidências.

---

## 8. Histórico de atualizações

| Data | Atualização |
|---|---|
| 2026-06-14 | Criação do plano: objetivo, estratégia, escopo, cenários de Login e Produtos e critérios de qualidade definidos antes da evolução do código. |
| 2026-06-15 | Implementação de `test_login_serverRest_api.py` (5 testes) e `test_produto_serverRest_api.py` (16 testes); cobertura recalculada com base na suíte real. Implementação do Extra 1 (JSON Schema) em `GET /usuarios`, `POST /login` e `GET /produtos`. README reestruturado como resumo enxuto, com este documento concentrando o detalhamento de cenários, cobertura e o bug encontrado. |
