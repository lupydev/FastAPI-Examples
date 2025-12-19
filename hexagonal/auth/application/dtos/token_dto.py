from pydantic import BaseModel, Field


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayloadDTO(BaseModel):
    sub: str = Field(description="User ID")
    exp: int = Field(description="Expiration time as a Unix timestamp")


class TokenDTO(TokenBase):
    """Internal use in application and domain layers."""

    pass


class TokenResponseDTO(TokenBase):
    """Used for responses to clients."""

    pass
