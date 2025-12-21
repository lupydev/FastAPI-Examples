from .base import DomainException


class UserAlreadyExistsException(DomainException):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message)
