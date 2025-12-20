from sqlmodel import SQLModel, create_engine

from .config import settings

engine = create_engine(
    str(settings.DB_URL),
    echo=True,
    future=True,
    connect_args={"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {},
)


def init_db():
    from ..adapters.persistence import __all__  # noqa: F401

    SQLModel.metadata.create_all(engine)
