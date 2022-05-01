from contextlib import AbstractContextManager
from datetime import date
from typing import Callable
from sqlalchemy.orm import Session, joinedload

from src.schemas import Transaction, MarketTransaction, ResourceTransaction, ServiceTransaction

class TransactionRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
    
    def findAll(self):
        with self.session_factory() as db:
            return db.query(Transaction).all()

    def findAllMarketTransactions(self):
        with self.session_factory() as db:
            return db.query(MarketTransaction).all()
    
    def findAllServiceTransactions(self):
        with self.session_factory() as db:
            return db.query(ServiceTransaction).options(joinedload(ServiceTransaction.serviceIds)).all()

    def findAllResourceTransactions(self):
        with self.session_factory() as db:
            return db.query(ResourceTransaction).options(joinedload(ResourceTransaction.resourceIds)).all()

    def findById(self, transactionId: int):
        with self.session_factory() as db:
            return db.query(Transaction).filter(Transaction.id == transactionId).first()

    def findAllByCreatedAt(self, createdAt: date):
        with self.session_factory() as db:
            return db.query(Transaction).filter(Transaction.createdAt == createdAt).all()

    def findByUserId(self, userId: int):
        with self.session_factory() as db:
            return db.query(Transaction).filter(Transaction.userId == userId).all()
            
    def create(self, tx: any):
        with self.session_factory() as db:
            db.add(tx)
            db.commit()
            db.refresh(tx)
            return tx
        
    def update(self, tx: any):
        with self.session_factory() as db:
            db.add(tx)
            db.commit()
            db.refresh(tx)
            return tx