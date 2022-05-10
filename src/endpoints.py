from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, status
from dependency_injector.wiring import inject, Provide
import fastapi

from src.containers import Container
from src.models import PayRequestBody, TransactionCreate, MarketTransactionCreate, ServiceTransactionCreate, ResourceTransactionCreate
from src.enums import TransactionStatus, TransactionsFilter
from src.services import TransactionService
from src.integrations import UserService


router = APIRouter()

@router.post("/api/v1/pay")
@inject
def pay(
    body: PayRequestBody,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Client") or
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    status = 0
    try:
        if(body.txBase != None):
            status = transactionService.pay(body.txBase)
        elif(body.txMarket != None):
            status = transactionService.pay(body.txMarket)
        elif(body.txService != None):
            status = transactionService.pay(body.txService)
        elif(body.txResource != None):
            status = transactionService.pay(body.txResource)
    except:
        raise HTTPException(status.HTTP_409_CONFLICT, "Cound't create transactions")
    finally:
        return status
        
@router.get("/api/v1/create-invoice/{transactionId}")
@inject
def createInvoice(
    transactionId: int,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
        
    return fastapi.responses.StreamingResponse(
        transactionService.createInvoice(transactionId), 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document") 

@router.get("/api/v1/transactions")
@inject
def transactions(
    
    which: Optional[TransactionsFilter] = None,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")

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
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.findAllByCreatedAt(date)

@router.post("/api/v1/transactions-by-userid")
@inject
def transactionsByUserId(
    userId: int,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.findAllByUserId(userId)

@router.get("/api/v1/transaction/{id}")
@inject
def transaction(
    id: int,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.findById(id)

@router.post("/api/v1/transaction/create-market")
@inject
def create(
    transaction: MarketTransactionCreate,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.createMarket(transaction)

@router.post("/api/v1/transaction/create-service")
@inject
def create(
    transaction: ServiceTransactionCreate,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.createService(transaction)

@router.post("/api/v1/transaction/create-resource")
@inject
def create(
    transaction: ResourceTransactionCreate,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.createResource(transaction)

@router.post("/api/v1/transaction/create-base")
@inject
def create(
    transaction: TransactionCreate,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Employee") or
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.createBase(transaction)
    
@router.post("/api/v1/transaction/{id}/set-status")
@inject
def setStatus(
    id: int, 
    status: TransactionStatus,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.setTransactionStatus(id, status)

@router.get("/api/v1/daily-report")
@inject
def getDailyReport(
    date: date,
    Authorization: Optional[str] = Header(None),
    userService: UserService = Depends(Provide[Container.userService]),
    transactionService: TransactionService = Depends(Provide[Container.transactionService])
):
    if(Authorization == None):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to authenticate first")
    
    if(
        not userService.userContainsRole(Authorization, "Admin")
    ):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden access to this endpoint")
    
    return transactionService.getDailyReportForDate(date)