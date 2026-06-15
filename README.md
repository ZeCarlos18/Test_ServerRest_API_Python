# Testes Automatizados - ServeRest API

Suíte de testes automatizados em **Python + Pytest + Requests** para os endpoints de **Usuários**, **Login** e **Produtos** da [API ServeRest](https://compassuol.serverest.dev/).

Este projeto começou no **Desafio Semana 3** do Bootcamp QA (testes de Usuários) e foi evoluído para uma suíte mais completa: planejamento formal, expansão de cobertura (Login e Produtos), validação de JSON Schema (Extra 1), cálculo de cobertura e análise de divergências em relação ao Swagger.

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

## 🐞 Bug encontrado

Nenhuma divergência real de schema foi confirmada até o momento — o caso anteriormente apontado em `GET /usuarios/{_id}` era, na verdade, dois cenários distintos sendo testados juntos (formato de id inválido vs. id em formato válido porém inexistente), e a API responde corretamente em ambos conforme o Swagger.

Análise completa: [PLANO-DE-TESTES.md, seção 7](PLANO-DE-TESTES.md#7-divergências-entre-a-api-e-o-schema-documentado-no-swagger). O requisito de reportar pelo menos 1 bug na aba [Issues](../../issues) segue pendente.

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
