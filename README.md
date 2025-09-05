# API Financeira - Microserviço

Este repositório contém uma API REST para gerenciamento de operações financeiras, desenvolvida com FastAPI e Python.

## Sumário

- [Introdução](#introdução)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Introdução

A API Financeira oferece recursos para gerenciamento completo de operações financeiras, incluindo:
- Criação e gerenciamento de contas
- Cadastro de transações (receitas e despesas)
- Consulta de saldos por conta
- Filtros por categoria e conta
- Operações CRUD completas para transações

## Tecnologias

- **FastAPI** - Framework web moderno e rápido para Python
- **SQLAlchemy** - ORM para Python
- **MySQL** - Banco de dados relacional
- **Docker** - Containerização da aplicação
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

## Instalação

### Usando Docker (Recomendado)

```powershell
git clone https://github.com/elizaaugusta4/Api-financeira-microservico.git
cd Api-financeira-microservico
docker-compose up --build
```

Configure as variáveis de ambiente para conexão com o banco MySQL.

## Uso

```powershell
docker-compose up --build
```

Acesse `http://localhost:8000` para utilizar a API.

A documentação interativa estará disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Contas

| Método | Rota                    | Descrição                    |
|--------|-------------------------|------------------------------|
| POST   | /accounts               | Cria uma nova conta          |
| GET    | /accounts               | Lista todas as contas        |
| GET    | /accounts/{account_id}  | Busca uma conta específica   |

### Transações

| Método | Rota                        | Descrição                      |
|--------|-----------------------------|--------------------------------|
| POST   | /transactions               | Cria uma nova transação        |
| GET    | /transactions               | Lista todas as transações      |
| GET    | /transactions/{tx_id}       | Busca uma transação específica |
| PUT    | /transactions/{tx_id}       | Atualiza uma transação         |
| DELETE | /transactions/{tx_id}       | Remove uma transação           |

### Saldo

| Método | Rota                          | Descrição                    |
|--------|-------------------------------|------------------------------|
| GET    | /accounts/{account_id}/balance| Consulta o saldo de uma conta|

### Outros

| Método | Rota     | Descrição               |
|--------|----------|-------------------------|
| GET    | /        | Informações da API      |
| GET    | /health  | Status de saúde da API  |

## Estrutura do Projeto

```
Api-financeira-microservico/
├── app/
│   ├── __init__.py
│   ├── app.py          # Aplicação principal FastAPI
│   ├── database.py     # Configuração do banco de dados
│   ├── models.py       # Modelos SQLAlchemy
│   └── schemas.py      # Schemas Pydantic
├── docker-compose.yml  # Orquestração dos containers
├── Dockerfile          # Imagem da aplicação
├── requirements.txt    # Dependências Python
└── README.md           # Documentação
```

### Exemplos de Uso

#### Criar uma conta
```bash
curl -X POST "http://localhost:8000/accounts" ^
     -H "Content-Type: application/json" ^
     -d '{"name": "Conta Principal", "description": "Minha conta principal"}'
```

#### Criar uma transação
```bash
curl -X POST "http://localhost:8000/transactions" ^
           -H "Content-Type: application/json" ^
           -d '{
                "account_id": 1,
                "type": "INCOME",
                "amount": 1000.00,
                "description": "Salário",
                "category": "trabalho"
           }'
```

#### Consultar saldo
```bash
curl "http://localhost:8000/accounts/1/balance"
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
