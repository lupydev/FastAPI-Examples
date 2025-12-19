from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.main import api_routers
from .infrastructure.config.config import settings
from .infrastructure.config.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # shutdown logic here (if needed)


app = FastAPI(
    description="An authentication service using Hexagonal Architecture.",
    title=settings.PROJECT_NAME,
    version="0.0.1",
    lifespan=lifespan,
)

app.include_router(api_routers, prefix=settings.API)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
