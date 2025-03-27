from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select
from ...core.security import limiter
from ...models.user import User
from ...core.db import get_db
from ...schemas.user import ResponseUser, CreateUser, UserResponse
from ...schemas.pagination import PaginationParams, PaginatedResponse
from math import ceil

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
@limiter.limit("5/minute")  # Limita a 5 solicitudes por minuto
async def create_user(
    request: Request,
    user: CreateUser,
    db: Session = Depends(get_db),
):

    existing_email = db.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya existe",
        )

    existing_username = db.exec(
        select(User).where(User.username == user.username)
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe",
        )

    try:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse(results=new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}",
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[ResponseUser],
)
@limiter.limit("2/minute")  # Limita a 20 solicitudes por minuto
async def get_users(
    request: Request,
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
):
    """
    Obtiene la lista de usuarios con paginación y ordenamiento.

    Returns:
        Respuesta paginada con lista de usuarios y metadatos
    """
    try:
        # Validar el campo de ordenamiento
        if not hasattr(User, pagination.sort_by):
            pagination.sort_by = "created_at"

        # Calcular el valor de skip basado en la página y tamaño de página
        skip = (pagination.page - 1) * pagination.page_size

        # Contar el total de registros para los metadatos de paginación
        total_records = len(db.exec(select(User)).all())

        # Construir la consulta con ordenamiento dinámico
        sort_field = getattr(User, pagination.sort_by)
        query = select(User)

        if pagination.order.lower() == "asc":
            query = query.order_by(sort_field.asc())
        else:
            query = query.order_by(sort_field.desc())

        # Aplicar paginación
        query = query.offset(skip).limit(pagination.page_size)

        # Ejecutar la consulta
        users = db.exec(query).all()

        # Calcular metadatos de paginación
        total_pages = (
            ceil(total_records / pagination.page_size) if total_records > 0 else 0
        )

        # Construir respuesta paginada
        return PaginatedResponse(
            results=users,
            total=total_records,
            page=pagination.page,
            page_size=pagination.page_size,
            pages=total_pages,
            has_next=pagination.page < total_pages,
            has_previous=pagination.page > 1,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los usuarios: {str(e)}",
        )
