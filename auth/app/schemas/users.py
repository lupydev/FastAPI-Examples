from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import Field


class CreateUser(BaseModel):
    username: str = Field(
        nullable=False,
        min_length=2,
        unique=True,
    )
    email: EmailStr = Field(
        nullable=False,
        unique=True,
    )
    password: str = Field(
        nullable=False,
        min_length=3,
    )


class UpdateUser(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=2,
    )
    username: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(
        None,
        min_length=3,
    )
