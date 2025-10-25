# 💰 API Financeira com Monitoramento

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MySQL](https://img.shields.io/badge/mysql-8.0-blue.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

Uma API REST moderna para gerenciamento de operações financeiras com sistema completo de monitoramento e observabilidade.

## 🚀 Tecnologias

### Aplicacao
- **FastAPI** - Framework web moderno e de alta performance
- **SQLAlchemy** - ORM avançado para Python
- **MySQL 8.0** - Banco de dados relacional
- **Pydantic** - Validação e serialização de dados
- **Uvicorn** - Servidor ASGI de alto desempenho

## ⚡ Início Rápido

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) 
- [Git](https://git-scm.com/)

## 🌐 Endpoints da API

### 🏦 Contas

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `POST` | `/accounts` | Criar nova conta | 201 |
| `GET` | `/accounts` | Listar todas as contas | 200 |
| `GET` | `/accounts/{id}` | Buscar conta por ID | 200 |

### 💸 Transações

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|---------|
| `POST` | `/transactions` | Criar transação | 201 |
| `GET` | `/transactions` | Listar transações | 200 |
| `GET` | `/transactions/{id}` | Buscar transação | 200 |
| `PUT` | `/transactions/{id}` | Atualizar transação | 200 |
| `DELETE` | `/transactions/{id}` | Remover transação | 204 |

### 💰 Saldo

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/accounts/{id}/balance` | Consultar saldo da conta |

### 🔧 Sistema

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Informações da API |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Métricas Prometheus |
| `GET` | `/db-metrics` | Métricas do banco (debug) |

## 📁 Estrutura do Projeto

```
Api-financeira-microservico/
├── 📁 app/                          # Código da aplicação
│   ├── __init__.py
│   ├── app.py                       # App principal FastAPI
│   ├── database.py                  # Configuração BD
│   ├── models.py                    # Modelos SQLAlchemy
│   └── schemas.py                   # Schemas Pydantic
├── 📁 monitoring/                   # Configurações de monitoramento
│   ├── prometheus.yml               # Config Prometheus
│   └── 📁 grafana/
│       └── 📁 provisioning/
│           └── 📁 datasources/
│               └── prometheus.yml   # DataSource Grafana
├── 📁 K8s/                          # Configurações de kubernetes
│   ├── Deployment.yml               # Configuração de Deployment
├── Dockerfile                       # Imagem da API
├── requirements.txt                 # Deps Python
├── .my.cnf                         # Config MySQL Exporter
└── README.md                       # Esta documentação
```

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).


<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

Desenvolvido com ❤️ por [Eliza Augusta](https://github.com/elizaaugusta4)

</div>
