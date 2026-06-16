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

A suíte deve servir como base de regressão, podendo ser executada localmente e automaticamente via CI a cada push.

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
- **Extra 2** (✅ implementado): pipeline de GitHub Actions executando a suíte a cada push — `.github/workflows/tests.yml`

### 3.2. Fora de escopo

- **Carrinho** (`/carrinhos` e rotas relacionadas) — não solicitado neste desafio
- Testes de **performance/carga** (volume de requisições, tempo de resposta sob estresse)
- Testes de **segurança aprofundada** (fuzzing, SQL injection, etc.) além do que surgir naturalmente da validação de entradas
- Testes de **concorrência** (execução paralela / condições de corrida)
- Testes de **expiração de token** (os 600s de validade do token de login não serão testados via espera real, por inviabilidade de tempo de execução)
- Testes de **interface (UI)** — a suíte é 100% via API

---

## 4. Cenários a implementar (por endpoint)

### 4.1. Usuários — `test_serverRest_api.py` (Status: ✅ implementado — 12 testes)

| # | Cenário | Teste | Resultado esperado |
|---|---|---|---|
| 1 | Listar todos os usuários | `test_listar_usuarios` | 200, estrutura `{quantidade, usuarios[]}` |
| 2 | Listar usuários filtrando por nome | `test_listar_usuarios_por_nome` | 200, resultado contém usuário criado |
| 3 | Listar usuários filtrando por e-mail | `test_listar_usuarios_por_email` | 200, exatamente 1 resultado |
| 4 | Cadastrar usuário com dados válidos | `test_criar_usuario_com_sucesso` | 201, retorna `{message, _id}` (conforme schema `cadastroComSucesso` do Swagger) |
| 5 | Cadastrar usuário com e-mail duplicado | `test_criar_usuario_com_email_duplicado` | 400, mensagem menciona "email" |
| 6 | Cadastrar usuário sem o campo `nome` | `test_criar_usuario_sem_nome` | 400, retorna `{nome: "nome é obrigatório"}` |
| 7 | Buscar usuário por ID válido | `test_buscar_usuario_por_id` | 200, dados completos do usuário |
| 8 | Buscar usuário por ID com formato inválido (≠ 16 caracteres) | `test_buscar_usuario_por_id_formato_invalido` | 400, retorna `{id: "id deve ter exatamente 16 caracteres alfanuméricos"}` |
| 9 | Buscar usuário por ID com formato válido (16 caracteres alfanuméricos), porém inexistente | `test_buscar_usuario_por_id_nao_encontrado` | 400, retorna `{message: "Usuário não encontrado"}` (conforme schema `usuarioNaoEncontrado` do Swagger) |
| 10 | Excluir usuário existente | `test_excluir_usuario` | 200, mensagem de confirmação |
| 11 | Editar usuário existente | `test_editar_usuario` | 200, retorna `{message}` (conforme schema `alteradoComSucesso`); dados atualizados confirmados via `GET /usuarios/{_id}` |
| 12 | (Extra 1) Validar schema de `GET /usuarios` | `test_schema_listar_usuarios` | 200, resposta valida contra `SCHEMA_LISTAR_USUARIOS` |

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

A suíte soma **33 testes** em 3 arquivos: `test_serverRest_api.py` (Usuários, 12 testes), `test_login_serverRest_api.py` (Login, 5 testes) e `test_produto_serverRest_api.py` (Produtos, 16 testes) — incluindo os 3 testes de JSON Schema do Extra 1. Os 33 testes passam 100%.

### 6.3. Cenários que ficaram fora (e por quê)

- **Endpoint `/carrinhos`** (3 *paths*, 5 operações): não foi solicitado neste desafio. É o principal responsável pela diferença entre 56%/69% e 100% de Path/Operator Coverage — incluí-lo elevaria a cobertura total, mas está fora do escopo definido na seção 3.2.
- **Expiração do token de login (600s)**: testar o cenário real de expiração exigiria aguardar 10 minutos por execução (ou manipular o relógio do servidor), o que é inviável para a suíte de regressão. O comportamento de token *ausente/inválido* (401/403) é coberto via Produtos.
- **Status codes de erro de servidor (5xx)**: não são documentados oficialmente por operação e dependem de falhas internas não reproduzíveis sob demanda; portanto não fazem parte do denominador de Status Code Coverage.
- **Testes de carga, concorrência e segurança aprofundada (fuzzing, SQL injection, etc.)**: fora do objetivo funcional desta suíte (ver seção 3.2).

---

## 7. Divergências entre a API e o schema documentado no Swagger

A primeira versão deste plano apontava 4 falhas em `test_serverRest_api.py` como um único "bug de schema". Ao comparar a resposta real com o `swagger.json` publicado pela própria API (`https://compassuol.serverest.dev/swagger.json`), as 4 falhas se mostraram **erro de asserção/cenário nos nossos testes** (a API já respondia exatamente como o Swagger documenta, ou o teste exercitava um cenário diferente do documentado) e foram corrigidas. Após a correção, os 12 testes de `test_serverRest_api.py` passam 100%.

### 7.1. Casos descartados (API correta, teste estava errado)

| Operação | Schema documentado (`swagger.json`) | Resposta real | Conclusão |
|---|---|---|---|
| `POST /usuarios` (sucesso) | `cadastroComSucesso` = `{ "message", "_id" }` | `{ "message": "Cadastro realizado com sucesso", "_id": "..." }` | Bate com o documentado. `test_criar_usuario_com_sucesso` exigia eco de `nome`/`email`/`password`/`administrador`, que o Swagger nunca prometeu — teste corrigido. |
| `PUT /usuarios/{_id}` (sucesso) | `alteradoComSucesso` = `{ "message" }` | `{ "message": "Registro alterado com sucesso" }` | Bate com o documentado. `test_editar_usuario` corrigido para validar `message` e, adicionalmente, confirmar a alteração via `GET /usuarios/{_id}`. |
| `GET /usuarios/{_id}` com id inexistente | `usuarioNaoEncontrado` = `{ "message": "Usuário não encontrado" }` | Com um id de **15 caracteres** (`"123456789123456"`), a API retorna `{ "id": "id deve ter exatamente 16 caracteres alfanuméricos" }` | Não é divergência de schema: são **dois cenários diferentes**. O Swagger documenta `usuarioNaoEncontrado` para um id com o **formato válido** (16 caracteres alfanuméricos) que não existe na base — e a API responde exatamente isso (`{ "message": "Usuário não encontrado" }`). O teste original usava um id com **formato inválido** (15 caracteres), que aciona uma validação de formato distinta, anterior à busca do registro. Os dois cenários agora têm testes próprios: `test_buscar_usuario_por_id_formato_invalido` (formato inválido) e `test_buscar_usuario_por_id_nao_encontrado` (formato válido, id inexistente — confere com o schema `usuarioNaoEncontrado` do Swagger). |

### 7.2. Observação (não é bug): `POST /usuarios` sem campo obrigatório retorna formato não documentado

Para `POST /usuarios` sem o campo `nome`, a API retorna `{ "nome": "nome é obrigatório" }`. O Swagger **não documenta nenhum schema de 400 para esse cenário** (o único 400 documentado para `POST /usuarios` é o de e-mail duplicado, `errorEmailJaUtilizado`). Portanto isso não é uma divergência de um schema existente, e sim uma **lacuna de documentação**.

O mesmo padrão (`{<campo>: "<campo> é obrigatório"}`) ocorre também em `/login` e `/produtos`, e já é validado como comportamento real pelos testes em `test_login_serverRest_api.py` e `test_produto_serverRest_api.py`.

### 7.3. Nenhuma divergência de schema confirmada

Após a revisão acima, **nenhuma das divergências originalmente apontadas se confirmou como bug real** — todas eram erro de asserção ou de cenário nos testes, já corrigidos.

---

## 8. Bugs confirmados na API

Bugs descobertos por investigação manual (chamadas HTTP diretas, fora da suíte automatizada de regressão), comparando o comportamento real da API com o comportamento esperado segundo as boas práticas de REST e a consistência interna da própria API (endpoint `/produtos` como referência de implementação correta).

### 8.1. [BUG-01] `DELETE /usuarios/{_id}` não exige autenticação — exclusão anônima de usuário

| Item | Detalhe |
|---|---|
| **Endpoint** | `DELETE /usuarios/{_id}` |
| **Severidade** | Crítica |
| **Comportamento esperado** | Retornar `401 Unauthorized` quando nenhum token é enviado; retornar `403 Forbidden` quando o token pertence a um usuário não administrador |
| **Comportamento observado** | Retorna `200 OK` com `{"message": "Registro excluído com sucesso"}` sem nenhum token no header `Authorization` |
| **Evidência** | `DELETE /usuarios/{id_existente}` (sem header `Authorization`) → `200 OK` `{"message": "Registro excluído com sucesso"}`. Confirmado que o usuário é de fato removido (GET subsequente retorna `{"message": "Usuário não encontrado"}`). |
| **Referência de comportamento correto** | `DELETE /produtos/{_id}` sem token → `401 Unauthorized`. O endpoint de produtos implementa corretamente a proteção ausente em `/usuarios`. |
| **Impacto** | Qualquer pessoa com o ID de um usuário pode excluí-lo permanentemente sem credenciais. |
| **Reportado em** | [Issue #1](https://github.com/ZeCarlos18/Test_ServerRest_API_Python/issues/1) — *DELETE /usuarios/{id} não requer autenticação* |

**Comparativo direto:**

| Cenário | `DELETE /produtos/{_id}` | `DELETE /usuarios/{_id}` |
|---|---|---|
| Sem token | `401` ✅ | `200` ❌ BUG |
| Token de não-admin | `403` ✅ | `200` ❌ BUG |
| Token de admin | `200` ✅ | `200` ✅ |

---

### 8.2. [BUG-02] `PUT /usuarios/{_id}` não exige autenticação — edição anônima com escalada de privilégios

| Item | Detalhe |
|---|---|
| **Endpoint** | `PUT /usuarios/{_id}` |
| **Severidade** | Crítica |
| **Comportamento esperado** | Retornar `401 Unauthorized` quando nenhum token é enviado; retornar `403 Forbidden` quando o token pertence a um usuário não administrador |
| **Comportamento observado** | Retorna `200 OK` com `{"message": "Registro alterado com sucesso"}` sem nenhum token no header `Authorization`, aplicando todas as alterações enviadas no body — inclusive o campo `administrador` |
| **Evidência** | (1) Criar usuário com `"administrador": "false"`. (2) Enviar `PUT /usuarios/{id}` sem token, com body `{"administrador": "true", ...}`. (3) `GET /usuarios/{id}` confirma `"administrador": "true"`. A escalada de privilégios é efetivada. |
| **Referência de comportamento correto** | `PUT /produtos/{_id}` sem token → `401 Unauthorized`. O endpoint de produtos implementa corretamente a proteção ausente em `/usuarios`. |
| **Impacto** | Qualquer pessoa com o ID de um usuário pode: (a) alterar nome, e-mail ou senha de qualquer usuário; (b) promover um usuário comum a administrador, obtendo acesso total às rotas de `/produtos`. |
| **Reportado em** | [Issue #2](https://github.com/ZeCarlos18/Test_ServerRest_API_Python/issues/2) — *PUT /usuarios/{id} não requer autenticação e permite escalada de privilégios* |

**Comparativo direto:**

| Cenário | `PUT /produtos/{_id}` | `PUT /usuarios/{_id}` |
|---|---|---|
| Sem token | `401` ✅ | `200` ❌ BUG |
| Token de não-admin | `403` ✅ | `200` ❌ BUG |
| Token de admin | `200` ✅ | `200` ✅ |

---

## 9. Histórico de atualizações

| Data | Atualização |
|---|---|
| 2026-06-14 | Criação do plano: objetivo, estratégia, escopo, cenários de Login e Produtos e critérios de qualidade definidos antes da evolução do código. |
| 2026-06-15 | Implementação de `test_login_serverRest_api.py` (5 testes) e `test_produto_serverRest_api.py` (16 testes); cobertura recalculada com base na suíte real. Implementação do Extra 1 (JSON Schema) em `GET /usuarios`, `POST /login` e `GET /produtos`. README reestruturado como resumo enxuto, com este documento concentrando o detalhamento de cenários, cobertura e o bug encontrado. |
| 2026-06-15 | Análise do bug revisada contra o `swagger.json` real: 2 das 4 falhas eram asserções incorretas em `test_criar_usuario_com_sucesso` e `test_editar_usuario` (corrigidas — a API já seguia o schema documentado). A suíte de Usuários passa 100% (11/11). A única divergência real de schema confirmada é a do `GET /usuarios/{_id}` com id inválido (seção 7.2), a ser reportada nas Issues. |
| 2026-06-15 | Reanálise do item de `GET /usuarios/{_id}`: o cenário antes apontado como "bug" usava um id de 15 caracteres (formato inválido), que aciona uma validação de formato — não o caso `usuarioNaoEncontrado` do Swagger. Com um id de 16 caracteres alfanuméricos inexistente, a API responde exatamente `{message: "Usuário não encontrado"}`, conforme documentado. Não é bug. O teste original foi renomeado para `test_buscar_usuario_por_id_formato_invalido` e foi adicionado `test_buscar_usuario_por_id_nao_encontrado` (12 testes em `test_serverRest_api.py`, 33 na suíte). Nenhuma divergência real de schema permanece confirmada (seção 7.3); o requisito de reportar 1 bug segue pendente. |
| 2026-06-16 | Investigação manual além da suíte automatizada: encontrados 2 bugs críticos de ausência de autenticação em `DELETE /usuarios/{_id}` e `PUT /usuarios/{_id}` (seção 8). Ambos reportados na aba Issues do GitHub. O requisito de reportar pelo menos 1 bug está cumprido. |
| 2026-06-16 | Implementação do Extra 2: pipeline de CI criado em `.github/workflows/tests.yml` — roda `pytest -v` automaticamente a cada push ou pull request na branch `main`. |
