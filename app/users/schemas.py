from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    role_id: int
    password: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserPost(BaseModel):
    title: str
    content: str
    published: bool
    rating: int
    id: int


class UserGet(UserBase):
    id: int
    updated_at: datetime
    created_at: datetime
    posts: List[UserPost]
    liked_posts: List[UserPost]

    class Config:
        orm_mode = True
