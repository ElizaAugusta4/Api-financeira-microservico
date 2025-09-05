from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import time
import sys

from . import models
from . import schemas
from .database import get_db, engine

app = FastAPI(title="API Financeira", version="1.0.0")

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

@app.get("/")
def read_root():
    return {"message": "API Financeira está funcionando!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API está saudável"}

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