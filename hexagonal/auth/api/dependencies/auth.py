from typing import Annotated

from fastapi import Depends

from ...application.use_cases.auth.register_user import RegisterUserUseCase
from .infrastructure import SecurityDep
from .repositories import UserRepositoryDep


def get_register_user_use_case(
    user_repository: UserRepositoryDep,
    security_service: SecurityDep,
) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        user_repository=user_repository,
        security_service=security_service,
    )


RegisterUserUseCaseDep = Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)]
