from abc import ABC, abstractmethod
from typing import Any


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, sub: str) -> str:
        """Create a JWT access token."""
        pass

    @abstractmethod
    def create_refresh_token(self, sub: str) -> str:
        """Create a JWT refresh token."""
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str, Any]:
        """Decode a JWT access token."""
        pass

    @abstractmethod
    def decode_refresh_token(self, token: str) -> dict[str, Any]:
        """Decode a JWT refresh token."""
        pass
