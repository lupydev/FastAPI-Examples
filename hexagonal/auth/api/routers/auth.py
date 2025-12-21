from fastapi import APIRouter, HTTPException, status

from hexagonal.auth.domain.exceptions import (
    UserAlreadyExistsException,
)

from ...application.dtos import UserResponseDTO
from ...application.dtos.user_dto import UserCreateDTO
from ..dependencies.auth import RegisterUserUseCaseDep

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserCreateDTO,
    use_case: RegisterUserUseCaseDep,
):
    try:
        return use_case.execute(data)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
