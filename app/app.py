from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import time
import sys
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge
import psutil
import threading

from . import models
from . import schemas
from .database import get_db, engine

app = FastAPI(title="API Financeira", version="1.0.0")

# Configurar instrumentação do Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Métricas customizadas de sistema (apenas da aplicação)
cpu_usage = Gauge('app_cpu_usage_percent', 'CPU usage of the application process')
memory_usage = Gauge('app_memory_usage_bytes', 'Memory usage of the application process') 
memory_percent = Gauge('app_memory_usage_percent', 'Memory usage percentage of the application')

# Thread para coletar métricas de sistema
def collect_system_metrics():
    while True:
        try:
            # CPU da aplicação
            cpu_usage.set(psutil.cpu_percent(interval=1))
            
            # Memória da aplicação
            memory_info = psutil.virtual_memory()
            memory_usage.set(memory_info.used)
            memory_percent.set(memory_info.percent)
        except Exception as e:
            print(f"Erro ao coletar métricas de sistema: {e}")
        time.sleep(5)

# Iniciar coleta de métricas em background
threading.Thread(target=collect_system_metrics, daemon=True).start()

def create_tables():
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            models.Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso!")
            break
        except Exception as e:
            retry_count += 1
            print(f"Tentativa {retry_count}/{max_retries} falhou: {e}")
            if retry_count >= max_retries:
                print("Não foi possível conectar ao banco de dados após várias tentativas")
                sys.exit(1)
            time.sleep(2)

create_tables()

# Endpoint para métricas do banco (apenas para debug - dados vêm via mysql-exporter)
@app.get("/db-metrics")
def get_database_metrics(db: Session = Depends(get_db)):
    """Endpoint para verificar métricas do banco em tempo real (debug apenas)"""
    try:
        metrics = {}
        
        # Conexões ativas
        result = db.execute(text("SHOW STATUS LIKE 'Threads_connected'"))
        row = result.fetchone()
        metrics['active_connections'] = int(row[1]) if row else 0
        
        # Queries lentas
        result = db.execute(text("SHOW STATUS LIKE 'Slow_queries'"))
        row = result.fetchone()
        metrics['slow_queries'] = int(row[1]) if row else 0
        
        # Total de queries
        result = db.execute(text("SHOW STATUS LIKE 'Questions'"))
        row = result.fetchone()
        metrics['total_questions'] = int(row[1]) if row else 0
        
        # Threads rodando
        result = db.execute(text("SHOW STATUS LIKE 'Threads_running'"))
        row = result.fetchone()
        metrics['threads_running'] = int(row[1]) if row else 0
        
        return {"status": "ok", "mysql_metrics": metrics, "note": "Use mysql-exporter metrics for Prometheus"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter métricas: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API Financeira está funcionando!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API está saudável"}

# ... resto das rotas permanecem iguais ...
@app.post("/accounts", response_model=schemas.AccountOut, status_code=201)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    existing_account = db.query(models.Account).filter(models.Account.name == account.name).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Já existe uma conta com este nome")
    
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts", response_model=List[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()

@app.get("/accounts/{account_id}", response_model=schemas.AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account

@app.post("/transactions", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    account = db.query(models.Account).get(transaction.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions", response_model=List[schemas.TransactionOut])
def list_transactions(
    account_id: Optional[int] = Query(None, description="Filtrar por ID da conta"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    db: Session = Depends(get_db),
):
    q = db.query(models.Transaction)
    if account_id is not None:
        q = q.filter(models.Transaction.account_id == account_id)
    if category:
        q = q.filter(models.Transaction.category == category)
    return q.order_by(models.Transaction.occurred_at.desc(), models.Transaction.id.desc()).all()

@app.get("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def get_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return tx

@app.put("/transactions/{tx_id}", response_model=schemas.TransactionOut)
def update_transaction(tx_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    if transaction.account_id != tx.account_id:
        account = db.query(models.Account).get(transaction.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    for field, value in transaction.dict().items():
        setattr(tx, field, value)
    
    db.commit()
    db.refresh(tx)
    return tx

@app.delete("/transactions/{tx_id}", status_code=204)
def delete_transaction(tx_id: int, db: Session = Depends(get_db)):
    tx = db.query(models.Transaction).get(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    db.delete(tx)
    db.commit()
    return

@app.get("/accounts/{account_id}/balance", response_model=schemas.BalanceOut)
def get_balance(account_id: int, db: Session = Depends(get_db)):
    acc = db.query(models.Account).get(account_id)
    if not acc:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    income_sum = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0))
        .filter(models.Transaction.account_id == account_id)
        .filter(models.Transaction.type == "INCOME")
        .scalar()
    )
    expense_sum = (
        db.query(func.coalesce(func.sum(models.Transaction.amount), 0))
        .filter(models.Transaction.account_id == account_id)
        .filter(models.Transaction.type == "EXPENSE")
        .scalar()
    )
    return schemas.BalanceOut(
        account_id=account_id,
        income=income_sum,
        expense=expense_sum,
        balance=income_sum - expense_sum,
    )