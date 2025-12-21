from datetime import datetime
from uuid import uuid4

from ....domain.exceptions import UserAlreadyExistsException
from ....domain.models.user import User
from ....domain.ports.security_service import SecurityService
from ....domain.ports.user_repository import UserRepository
from ...dtos.user_dto import UserCreateDTO


class RegisterUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        security_service: SecurityService,
    ):
        self.user_repository = user_repository
        self.security_service = security_service

    def execute(self, user_data: UserCreateDTO) -> User:
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(user_data.email)

        hashed_password = self.security_service.hash_password(user_data.password)

        new_user = User(
            id=uuid4(),
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return self.user_repository.save(new_user)
