from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from .config import settings

engine = create_engine(
    str(settings.DB_URL),
    echo=True,
    future=True,
    connect_args={"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {},
)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    from ..adapters.persistence import __all__  # noqa: F401

    SQLModel.metadata.create_all(engine)


SessionDep = Annotated[Session, Depends(get_session)]
