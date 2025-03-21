from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ...models.user import User
from ...core.db import get_db
from ...schemas.users import ResponseUser, CreateUser

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=dict[str, ResponseUser]
)
async def create_user(
    user: CreateUser,
    db: Session = Depends(get_db),
):
    email = db.exec(select(User).where(User.email == user.email)).first()
    username = db.exec(select(User).where(User.username == user.username)).first()

    if username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"result": new_user}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, list[ResponseUser]],
)
async def get_users(db: Session = Depends(get_db)):
    users = db.exec(select(User).order_by(User.created_at.desc())).all()
    return {"result": users}
