from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    @field_validator("password")
    def validate_password(cls, v: str):
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe incluir al menos una letra minúscula.")

        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe incluir al menos una letra mayúscula.")

        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe incluir al menos un número.")

        special = "!@#$%^&*()_+-=[]{};':\"\\|,.<>/?"
        if not any(c in special for c in v):
            raise ValueError(f"La contraseña debe incluir al menos un carácter especial: {special}")

        return v


class UserResponseDTO(BaseModel):
    id: UUID
    email: EmailStr

    created_at: datetime
    is_active: bool
