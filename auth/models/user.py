from sqlmodel import Field, SQLModel, create_engine


class User(SQLModel, table=True):
    id: int | str = Field(
        default=None,
        primary_key=True,
    )
