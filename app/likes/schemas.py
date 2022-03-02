from pydantic import BaseModel


class LikeBase(BaseModel):
    post_id: int
    liked: bool
