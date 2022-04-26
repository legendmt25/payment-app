from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.enums import TransactionStatus

class TransactionBase(BaseModel):
    userId: int
    price: float

class MarketTransactionBase(TransactionBase):
    shoppingCartId: int

class ServiceTransactionBase(TransactionBase):
    petId: int
    serviceIds: list[int]

class ResourceTransactionBase(TransactionBase):
    petId: int
    resourceIds: list[int]

class TransactionCreate(TransactionBase):
    pass
class MarketTransactionCreate(MarketTransactionBase):
    pass
class ServiceTransactionCreate(ServiceTransactionBase):
    pass
class ResourceTransactionCreate(ResourceTransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    type: str
    createdAt: date
    status: TransactionStatus

    class Config:
        orm_mode = True

class MarketTransaction(Transaction):
    shoppingCartId: int
    class Config:
        orm_mode = True
class ServiceTransaction(Transaction):
    petId: int
    serviceIds: list
    class Config:
        orm_mode = True
class ResourceTransaction(Transaction):
    petId: int
    resourceIds: list
    class Config:
        orm_mode = True

class DailyReport(BaseModel):
    date: date
    totalTransactions: int
    totalResolved: int
    totalPending: int
    totalCanceled: int
    totalPrice: float



class PayRequestBody(BaseModel):
    txBase: Optional[TransactionCreate] = None
    txMarket: Optional[MarketTransactionCreate] = None
    txService: Optional[ServiceTransactionCreate] = None
    txResource: Optional[ResourceTransactionCreate] = None