from pydantic import BaseModel
class PostBase(BaseModel):
    title: str
    description: str | None = None

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
