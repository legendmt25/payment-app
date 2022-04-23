from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject

router = APIRouter()

@router.get("/init")
@inject
def init():
    return 'hello'