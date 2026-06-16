# Testes Automatizados - ServeRest API

Suíte de testes automatizados em **Python + Pytest + Requests** para os endpoints de **Usuários**, **Login** e **Produtos** da [API ServeRest](https://compassuol.serverest.dev/).

Este projeto começou no **Desafio Semana 3** do Bootcamp QA (testes de Usuários) e foi evoluído para uma suíte mais completa: planejamento formal, expansão de cobertura (Login e Produtos), validação de JSON Schema, pipeline de CI com GitHub Actions, cálculo de cobertura e reporte de bugs.

📄 **Para todos os detalhes — cenários por endpoint, critérios de qualidade, metodologia, cálculo de cobertura e análise das divergências encontradas — consulte o [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md).**

---

## 🚀 Instalação e execução

Requisitos: Python 3.8+, pip e conexão com a internet.

```bash
pip install -r requirements.txt
pytest -v        # roda toda a suíte
pytest -v -s     # com os prints de depuração
```

Suítes individuais:
```bash
pytest test_serverRest_api.py -v          # Usuários
pytest test_login_serverRest_api.py -v    # Login
pytest test_produto_serverRest_api.py -v  # Produtos
```

---

## 📁 Estrutura do projeto

```
Test_ServerRest_API_Python/
│
├── test_serverRest_api.py         # Testes de Usuários (Semana 3 + Extra 1)
├── test_login_serverRest_api.py   # Testes de Login
├── test_produto_serverRest_api.py # Testes de Produtos
├── PLANO-DE-TESTES.md             # Plano completo: cenários, cobertura, divergências
├── README.md                      # Este arquivo
└── requirements.txt                # Dependências
```

---

## 📊 Suíte de testes (resumo)

| Arquivo | Testes | Resultado |
|---|---|---|
| `test_serverRest_api.py` (Usuários) | 12 | 100% ✅ |
| `test_login_serverRest_api.py` (Login) | 5 | 100% ✅ |
| `test_produto_serverRest_api.py` (Produtos) | 16 | 100% ✅ |

Inclui 3 testes de **validação de JSON Schema**, um por arquivo. Lista completa de cenários, com o nome de cada função de teste: [PLANO-DE-TESTES.md, seção 4](PLANO-DE-TESTES.md#4-cenários-a-implementar-por-endpoint).

---

## 📈 Cobertura de testes

| Métrica | Resultado |
|---|---|
| Path Coverage | ≈ 56% (5/9 paths) |
| Operator Coverage | ≈ 69% (11/16 operações) |
| Status Code Coverage | 100% (5/5: 200, 201, 400, 401, 403) |

Metodologia aplicada, inventário da API e justificativa do que ficou fora do escopo (ex.: `/carrinhos`, expiração de token): [PLANO-DE-TESTES.md, seção 6](PLANO-DE-TESTES.md#6-cobertura-de-testes).

---

## 🐞 Bugs encontrados

Dois bugs críticos de ausência de autenticação foram encontrados por investigação manual no endpoint `/usuarios` e reportados na aba Issues do GitHub:

| ID | Endpoint | Descrição | Severidade |
|---|---|---|---|
| [BUG-01](https://github.com/ZeCarlos18/Test_ServerRest_API_Python/issues/1) | `DELETE /usuarios/{_id}` | Exclusão de qualquer usuário sem token — deveria exigir `401`/`403` | Crítica |
| [BUG-02](https://github.com/ZeCarlos18/Test_ServerRest_API_Python/issues/2) | `PUT /usuarios/{_id}` | Edição de qualquer usuário sem token, incluindo escalada de privilégios (`administrador: false → true`) — deveria exigir `401`/`403` | Crítica |

Em ambos os casos, o endpoint equivalente de `/produtos` (`DELETE /produtos/{_id}` e `PUT /produtos/{_id}`) implementa corretamente a proteção de autenticação, evidenciando a inconsistência.

Documentação completa dos bugs (comportamento esperado vs. observado, evidências e comparativo): [PLANO-DE-TESTES.md, seção 8](PLANO-DE-TESTES.md#8-bugs-confirmados-na-api).

---

## ⚙️ CI — GitHub Actions (Extra 2)

A suíte roda automaticamente a cada `push` ou `pull request` na branch `main`, via `.github/workflows/tests.yml`. O resultado (✅ ou ❌) aparece na aba **Actions** do repositório.

---

## 🛠️ Troubleshooting

- **`ModuleNotFoundError`**: rode `pip install -r requirements.txt`.
- **`ConnectionError`**: verifique a conexão com `https://compassuol.serverest.dev/`.
- **Falha inesperada em um teste**: rode com `-v -s --tb=long` para ver o corpo da resposta da API.

---

## 🌐 Referências

- **API ServeRest**: https://compassuol.serverest.dev/
- **Plano de testes completo**: [`PLANO-DE-TESTES.md`](PLANO-DE-TESTES.md)
- **Metodologia de cobertura**: [Como verificar a cobertura de testes da API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b)
