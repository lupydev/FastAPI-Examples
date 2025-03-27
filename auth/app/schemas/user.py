from uuid import UUID
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class CreateUser(SQLModel):
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


class UpdateUser(SQLModel):
    name: str | None = Field(
        default=None,
        min_length=2,
    )
    username: str | None = None
    email: EmailStr | None = None


class ResponseUser(SQLModel):
    id: UUID
    name: str | None = None
    surname: str | None = None
    username: str
    email: EmailStr


class UserResponse(SQLModel):
    user: ResponseUser
