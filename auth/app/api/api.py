from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import models
from db.engine import engine, SQLModel


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

app.include_router()
