from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationResponseDTO[T](BaseModel):
    total_items: int = Field(ge=0)
    page: int = Field(ge=1)
    size: int = Field(ge=1)
    total_pages: int = Field(ge=0)
    has_next: bool
    has_prev: bool
    items: list[T]
