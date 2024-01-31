from typing import Optional
from sqlmodel import Field
from models.abstract import Abstract


class User(Abstract, table=True):
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    username: Optional[str] = Field(
        nullable=False,
        min_length=2,
        unique=True,
    )
    email: Optional[str] = Field(
        nullable=False,
        unique=True,
    )
    password: Optional[str] = Field(
        nullable=False,
        min_length=3,
    )
