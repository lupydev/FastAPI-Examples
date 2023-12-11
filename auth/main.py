from fastapi import Depends, FastAPI
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI(
    title="Auth_api",
    description="Api para trabajar las diferentes autenticaciones y manejo de tokens",
    version="0.0.1",
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str
    disable: bool


def decode_token(token):
    return User(
        username=token + "fakedecode",
        email="example@example.com",
        disable=False,
    )


async def current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user


@app.get("/users/me")
async def read_user_me(current_user: Annotated[User, Depends(current_user)]):
    return current_user


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
