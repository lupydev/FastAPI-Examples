from abc import ABC, abstractmethod
from uuid import UUID

from ..models.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a user entity"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        """Retrieve a user by ID"""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> list[User]:
        """Retrieve all users with pagination"""
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """Delete a user entity"""
        pass

    @abstractmethod
    def count(self) -> int:
        """Count total number of users"""
        pass
