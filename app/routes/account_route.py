from fastapi import APIRouter
from isort import stream
from services.account_service import AccountService

router = APIRouter()

@router.get("/account")
async def account():
    """
    계좌 정보를 조회한다.
    """
    response = AccountService.accounts()
    print(response)
    return response
    