from fastapi import APIRouter
from core.config import settings

router = APIRouter()


@router.get("/")
async def get_users():
    return {"message": "Hello World"}
