from typing import Annotated

from fastapi import Depends

from ...domain.ports.user_repository import UserRepository
from ...infrastructure.adapters.persistence.sql_user_repository import SQLUserRepository
from .infrastructure import SessionDep


def get_user_repository(session: SessionDep) -> UserRepository:
    return SQLUserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
