from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.enums import TransactionStatus

class TransactionBase(BaseModel):
    price: float

class MarketTransactionBase(TransactionBase):
    shoppingCartId: int

class ServiceTransactionBase(TransactionBase):
    # petId: int
    serviceIds: list[int]

class ResourceTransactionBase(TransactionBase):
    # petId: int
    resourceIds: list[int]

class TransactionCreatePartial(TransactionBase):
    pass
class MarketTransactionCreatePartial(MarketTransactionBase):
    pass
class ServiceTransactionCreatePartial(ServiceTransactionBase):
    pass
class ResourceTransactionCreatePartial(ResourceTransactionBase):
    pass

class TransactionCreate(TransactionCreatePartial):
    userId: str

class MarketTransactionCreate(MarketTransactionCreatePartial):
    userId: str

class ServiceTransactionCreate(ServiceTransactionCreatePartial):
    userId: str

class ResourceTransactionCreate(ResourceTransactionCreatePartial):
    userId: str


class Transaction(TransactionBase):
    id: int
    type: str
    userId: str
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
    txBase: Optional[TransactionCreatePartial] = None
    txMarket: Optional[MarketTransactionCreatePartial] = None
    txService: Optional[ServiceTransactionCreatePartial] = None
    txResource: Optional[ResourceTransactionCreatePartial] = None