from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    username: str
    email: str


class LoginUser(BaseModel):
    username: str
    password: str
