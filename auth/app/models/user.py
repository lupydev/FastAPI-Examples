from sqlmodel import Field
from .abstract import Abstract
from pydantic import EmailStr


class User(Abstract, table=True):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    surname: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    username: str = Field(
        nullable=False,
        min_length=2,
        max_length=20,
        unique=True,
    )
    email: EmailStr = Field(unique=True)
    password: str = Field(min_length=3)
