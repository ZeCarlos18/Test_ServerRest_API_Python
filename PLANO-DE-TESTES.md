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
- **Extra 1**: validação de estrutura de resposta via JSON Schema em pelo menos 3 endpoints
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

### 4.1. Usuários — `/usuarios` (Status: ✅ implementado na Semana 3)

| # | Cenário | Resultado esperado |
|---|---|---|
| 1 | Listar todos os usuários | 200, estrutura `{quantidade, usuarios[]}` |
| 2 | Listar usuários filtrando por nome | 200, resultado contém usuário criado |
| 3 | Listar usuários filtrando por e-mail | 200, exatamente 1 resultado |
| 4 | Cadastrar usuário com dados válidos | 201, retorna `_id` e dados enviados |
| 5 | Cadastrar usuário com e-mail duplicado | 400, mensagem menciona "email" |
| 6 | Cadastrar usuário sem o campo `nome` | 400, mensagem menciona "nome" |
| 7 | Buscar usuário por ID válido | 200, dados completos do usuário |
| 8 | Buscar usuário por ID inválido | 400, mensagem de erro |
| 9 | Excluir usuário existente | 200, mensagem de confirmação |
| 10 | Editar usuário existente | 200, dados atualizados refletidos |

### 4.2. Login — `/login` (Status: ✅ implementado em `test_login_serverRest_api.py`)

| # | Cenário | Resultado esperado |
|---|---|---|
| 1 | Login com credenciais corretas (usuário cadastrado previamente) | 200, resposta contém `message` e `authorization` (`Bearer <token>`) |
| 2 | Login com senha errada | 401, mensagem "Email e/ou senha inválidos" |
| 3 | Login com e-mail inexistente | 401, mensagem "Email e/ou senha inválidos" |
| 4 | Login com campos vazios/ausentes (`email`/`password`) | 400, mensagem indicando campo obrigatório |

> O token obtido no cenário 1 também é reaproveitado como pré-condição (setup) dos testes de Produtos que exigem usuário administrador.

### 4.3. Produtos — `/produtos` e `/produtos/{_id}` (Status: ✅ implementado em `test_produto_serverRest_api.py`)

| # | Cenário | Resultado esperado |
|---|---|---|
| 1 | Listar produtos cadastrados | 200, estrutura `{quantidade, produtos[]}` |
| 2 | Listar produtos com filtro (ex: por `nome`) | 200, resultado coerente com filtro |
| 3 | Cadastrar produto com token de usuário **administrador** e nome único | 201, retorna `message` e `_id` |
| 4 | Cadastrar produto com nome já existente | 400, mensagem "Já existe produto com esse nome" |
| 5 | Cadastrar produto **sem token** | 401, mensagem de token ausente/inválido |
| 6 | Cadastrar produto com token de usuário **não administrador** | 403, mensagem "Rota exclusiva para administradores" |
| 7 | Buscar produto por ID válido | 200, dados do produto retornados |
| 8 | Buscar produto por ID inválido/inexistente | 400, mensagem "Produto não encontrado" |
| 9 | Atualizar (editar) produto existente com token de admin | 200, mensagem "Registro alterado com sucesso" |
| 10 | Atualizar produto com ID inexistente (cria novo registro) | 201, mensagem de cadastro realizado |
| 11 | Atualizar produto sem token | 401, mensagem de token ausente/inválido |
| 12 | Atualizar produto com token de usuário não administrador | 403, mensagem "Rota exclusiva para administradores" |
| 13 | Excluir produto existente com token de admin | 200, mensagem de exclusão |
| 14 | Excluir produto sem token | 401, mensagem de token ausente/inválido |
| 15 | Excluir produto com token de usuário não administrador | 403, mensagem "Rota exclusiva para administradores" |

> Fluxo de autenticação: para os cenários 3, 9 e 13 (operações que exigem admin), o teste cria um usuário com `administrador: "true"`, faz login em `/login` e usa o `authorization` retornado no header `Authorization` da requisição. Para os cenários 6, 12 e 15, é usado um usuário com `administrador: "false"`.

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

## 6. Cobertura de testes — metodologia (referência)

A cobertura da suíte será calculada com base nas dimensões propostas no artigo [*Como verificar a cobertura de testes da API REST*](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b). As métricas aplicadas a este projeto são:

- **Path Coverage**: `nº de endpoints (paths) com pelo menos 1 teste / nº total de paths da API`
- **Operator Coverage**: `nº de operações (método + path) testadas / nº total de operações da API`
- **Status Code Coverage**: `nº de status codes distintos validados pelos testes / nº total de status codes documentados para os endpoints em escopo`

O cálculo detalhado, com os números atuais e a explicação dos itens fora de escopo, está documentado no `README.md`, seção **Cobertura de Testes**. Esse cálculo será revisado a cada incremento relevante da suíte (inclusão de Login e de Produtos).

---

## 7. Histórico de atualizações

| Data | Atualização |
|---|---|
| 2026-06-14 | Criação do plano: objetivo, estratégia, escopo, cenários de Login e Produtos e critérios de qualidade definidos antes da evolução do código. |
