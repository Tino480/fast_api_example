from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.users.schemas import UserBase


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: int = 0


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None


class PostUserGet(UserBase):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class PostGet(PostBase):
    id: int
    updated_at: datetime
    created_at: datetime
    likes: int
    user: PostUserGet

    class Config:
        orm_mode = True
