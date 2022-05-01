from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from src.containers import Container

from src.models import PayRequestBody, TransactionCreate, MarketTransactionCreate, ServiceTransactionCreate, ResourceTransactionCreate
from src.enums import TransactionStatus, TransactionsFilter
from src.services import TransactionService

router = APIRouter()

@router.post("/api/v1/pay")
@inject
def pay(
    body: PayRequestBody,
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(body.txBase != None):
        return transactionService.pay(body.txBase)
    elif(body.txMarket != None):
        return transactionService.pay(body.txMarket)
    elif(body.txService != None):
        return transactionService.pay(body.txService)
    elif(body.txResource != None):
        return transactionService.pay(body.txResource)


@router.get("/api/v1/transactions")
@inject
def transactions(
    which: Optional[TransactionsFilter] = None,
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if which == TransactionsFilter.ALL or which == None:
        return transactionService.findAll()
    elif which == TransactionsFilter.MARKET:
        return transactionService.findAllMarketTransactions()
    elif which == TransactionsFilter.RESOURCE:
        return transactionService.findAllResourceTransactions()
    elif which == TransactionsFilter.SERVICE:
        return transactionService.findAllServiceTransactions()

@router.post("/api/v1/transactions-by-creation")
@inject
def transactionsByCreatedAt(
    date: date, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.findAllByCreatedAt(date)

@router.post("/api/v1/transactions-by-userid")
@inject
def transactionsByUserId(
    userId: int, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.findAllByUserId(userId)

@router.get("/api/v1/transaction/{id}")
@inject
def transaction(
    id: int, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.findById(id)

@router.post("/api/v1/transaction/create-market")
@inject
def create(
    transaction: MarketTransactionCreate, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.createMarket(transaction)

@router.post("/api/v1/transaction/create-service")
@inject
def create(
    transaction: ServiceTransactionCreate, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.createService(transaction)

@router.post("/api/v1/transaction/create-resource")
@inject
def create(
    transaction: ResourceTransactionCreate, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.createResource(transaction)

@router.post("/api/v1/transaction/create-base")
@inject
def create(
    transaction: TransactionCreate, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.createBase(transaction)
    
@router.post("/api/v1/transaction/{id}/set-status")
@inject
def setStatus(
    id: int, 
    status: TransactionStatus, 
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.setTransactionStatus(id, status)

@router.get("/api/v1/daily-report")
@inject
def getDailyReport(
    date: date,
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    return transactionService.getDailyReportForDate(date)