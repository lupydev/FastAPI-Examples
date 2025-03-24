from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import settings
from .api.main import api_router
from .core.db import engine
from sqlmodel import SQLModel
from slowapi.middleware import SlowAPIMiddleware
from .core.security import limiter


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Autenticacion",
    description="API para la creación y autenticación de usuarios",
    version="0.0.1",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.include_router(api_router, prefix=settings.API)
