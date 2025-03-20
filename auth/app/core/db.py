from typing import Generator
from sqlmodel import Session, create_engine, SQLModel

sqlite_url = "sqlite:///./auth.db"

engine = create_engine(sqlite_url, echo=True)


def get_db() -> Generator:
    with Session(engine) as session:
        yield session
