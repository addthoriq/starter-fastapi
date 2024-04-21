from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    description: str | None = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

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