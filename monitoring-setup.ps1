# Script para gerenciar o ambiente de monitoramento
# Use: .\monitoring-setup.ps1 [start|stop|restart|status|logs]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "cleanup")]
    [string]$Action
)

function Start-Monitoring {
    Write-Host "🚀 Iniciando serviços de monitoramento..." -ForegroundColor Green
    docker-compose up -d
    Start-Sleep 5
    
    Write-Host "`n📊 Serviços disponíveis:" -ForegroundColor Yellow
    Write-Host "• Grafana: http://localhost:3000 (admin/admin123)" -ForegroundColor Cyan
    Write-Host "• Prometheus: http://localhost:9090" -ForegroundColor Cyan
    Write-Host "• API Financeira: http://localhost:8888" -ForegroundColor Cyan
    Write-Host "• MySQL Exporter: http://localhost:9104/metrics" -ForegroundColor Cyan
    
    Show-Status
}

function Stop-Monitoring {
    Write-Host "⏹️ Parando serviços de monitoramento..." -ForegroundColor Red
    docker-compose stop prometheus grafana mysql-exporter
}

function Restart-Monitoring {
    Write-Host "🔄 Reiniciando serviços de monitoramento..." -ForegroundColor Yellow
    docker-compose restart prometheus grafana mysql-exporter
    Start-Sleep 3
    Show-Status
}

function Show-Status {
    Write-Host "`n📋 Status dos serviços:" -ForegroundColor Yellow
    docker-compose ps
}

function Show-Logs {
    Write-Host "📝 Mostrando logs dos serviços de monitoramento..." -ForegroundColor Blue
    docker-compose logs -f prometheus grafana mysql-exporter
}

function Cleanup-Monitoring {
    Write-Host "🧹 Limpando volumes e containers de monitoramento..." -ForegroundColor Magenta
    docker-compose down -v
    docker volume rm api-financeira-microservico_prometheus_data -f
    docker volume rm api-financeira-microservico_grafana_data -f
}

switch ($Action) {
    "start" { Start-Monitoring }
    "stop" { Stop-Monitoring }
    "restart" { Restart-Monitoring }
    "status" { Show-Status }
    "logs" { Show-Logs }
    "cleanup" { Cleanup-Monitoring }
}