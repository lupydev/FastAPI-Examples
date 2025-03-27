from typing import Generic, TypeVar
from pydantic import BaseModel, Field
from sqlmodel import SQLModel

T = TypeVar("T")


class PaginationParams(SQLModel):
    """Parámetros para controlar la paginación y ordenamiento"""

    page: int = Field(default=1, ge=1, description="Número de página actual")
    page_size: int = Field(
        default=5,
        ge=1,
        le=1000,
        description="Elementos por página",
    )
    sort_by: str = Field(
        default="created_at",
        description="Campo por el cual ordenar",
    )
    order: str = Field(
        default="desc",
        description="Dirección del ordenamiento ('asc' o 'desc')",
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada con metadatos"""

    total: int
    page: int
    page_size: int
    pages: int
    has_next: bool
    has_previous: bool
    results: list[T]
