from dataclasses import asdict
from uuid import UUID

from sqlmodel import Session, func, select

from ....domain.models.user import User
from ....domain.ports.user_repository import UserRepository
from .user import UserTable


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        new_user = UserTable.model_validate(asdict(user))
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return user

    def get_by_email(self, email: str) -> User | None:
        user = self.session.exec(select(UserTable).where(UserTable.email == email)).one_or_none()

        if not user:
            return None

        return User(**user.model_dump())

    def get_by_id(self, user_id: UUID) -> User | None:
        user = self.session.get(UserTable, user_id)

        if not user:
            return None

        return User(**user.model_dump())

    def update(self, user: User) -> User | None:
        update_user = self.session.get(UserTable, user.id)
        if not update_user:
            return None

        # Transform data class to dict
        data = asdict(user)
        data.pop("id", None)  # avoid updating the ID

        for key, value in data.items():
            setattr(update_user, key, value)

        self.session.add(update_user)
        self.session.commit()
        self.session.refresh(update_user)
        return User(**update_user.model_dump())

    def delete(self, user: User) -> None:
        user_db = self.session.get(UserTable, user.id)
        if user_db:
            self.session.delete(user_db)
            self.session.commit()

    def get_all(self, skip: int = 0, limit: int = 10) -> list[User]:
        users = self.session.exec(select(UserTable).offset(skip).limit(limit)).all()

        return [User(**user.model_dump()) for user in users]

    def count(self) -> int:
        return self.session.exec(select(func.count()).select_from(UserTable)).one()
