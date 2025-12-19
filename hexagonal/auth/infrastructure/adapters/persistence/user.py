from datetime import datetime
from typing import ClassVar
from pydantic import EmailStr
from sqlalchemy import Column
from sqlmodel import DateTime, SQLModel, Field, text
from uuid import UUID, uuid4


class UserTable(SQLModel, table=True):
    __tablename__: ClassVar[str] = "users"  # Specify table name

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        ),
    )
