from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from ...infrastructure.adapters.security.security_service import PasslibSecurityService
from ...infrastructure.config.db import engine


def get_session():
    with Session(engine) as session:
        yield session


def get_security_service():
    return PasslibSecurityService()


SessionDep = Annotated[Session, Depends(get_session)]
SecurityDep = Annotated[PasslibSecurityService, Depends(get_security_service)]
