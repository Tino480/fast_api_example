from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    exp: int
