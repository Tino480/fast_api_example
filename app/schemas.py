from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    exp: int


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


class LikeBase(BaseModel):
    post_id: int
    liked: bool
