from fastapi import APIRouter
from core.config import settings

router = APIRouter(
    prefix=f"{settings.API_V1_STR}",
    tags=["Users"],
)
