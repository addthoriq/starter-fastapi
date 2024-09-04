from pydantic import BaseModel
from .postModel import PostBase

class UserBase(BaseModel):
    email: str
    username: str
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class User(UserBase):
    id: int
    is_active: bool
    posts: list[PostBase] = []

    class Config:
        orm_mode = True