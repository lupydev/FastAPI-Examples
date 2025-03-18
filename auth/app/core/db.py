from typing import Generator
from sqlmodel import Session, create_engine, SQLModel
from core.config import Settings

engine = create_engine(Settings.DB_URL, echo=True)


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
