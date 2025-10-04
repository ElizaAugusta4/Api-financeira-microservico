# Monitoramento da API Financeira

Este setup inclui Prometheus e Grafana para monitoramento completo da API Financeira e do banco de dados MySQL.

## Serviços de Monitoramento

### Prometheus (http://localhost:9090)
- **Função**: Coleta e armazena métricas
- **Porta**: 9090
- **Configuração**: `monitoring/prometheus.yml`

### Grafana (http://localhost:3000)
- **Função**: Visualização de métricas e dashboards
- **Porta**: 3000
- **Credenciais padrão**: 
  - Usuário: `admin`
  - Senha: `admin123`

### MySQL Exporter (http://localhost:9104)
- **Função**: Exporta métricas do MySQL para o Prometheus
- **Porta**: 9104
- **Endpoint de métricas**: `/metrics`

## Como usar

1. **Subir todos os serviços**:
   ```bash
   docker-compose up -d
   ```

2. **Verificar se todos os serviços estão rodando**:
   ```bash
   docker-compose ps
   ```

## Métricas Disponíveis

### API FastAPI
- **Taxa de requisições**: `rate(http_requests_total[5m])`
- **Tempo de resposta**: `http_request_duration_seconds`
- **Status das requisições**: `http_requests_total`
- **Métricas de processo**: CPU, memória, etc.

### MySQL
- **Status do servidor**: `mysql_up`
- **Conexões ativas**: `mysql_global_status_connections`
- **Queries executadas**: `mysql_global_status_queries`
- **Performance**: `mysql_global_status_slow_queries`
- **Uso de memória**: `mysql_global_status_innodb_buffer_pool_pages_total`

## Dashboards

O dashboard principal inclui:
- **API Request Rate**: Taxa de requisições por segundo
- **API Response Time**: Tempo de resposta (percentis 50 e 95)
- **MySQL Status**: Status de conectividade do MySQL
- **MySQL Connections**: Número de conexões ativas

## Arquivos de Configuração

```
monitoring/
├── prometheus.yml              # Configuração do Prometheus
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml  # Configuração do datasource
│   │   └── dashboards/
│   │       └── dashboard.yml   # Configuração dos dashboards
│   └── dashboards/
│       └── api-dashboard.json  # Dashboard da API Financeira
```

## Endpoints de Métricas

- **API Financeira**: http://localhost:8888/metrics
- **MySQL Exporter**: http://localhost:9104/metrics
- **Prometheus**: http://localhost:9090/metrics

