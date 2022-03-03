from fastapi import HTTPException, Depends, status
from app.auth.services import get_current_user
from app.database import Base
from app.users.models import User
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Role(Base):
    __tablename__ = "roles"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="role")


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role.name not in self.allowed_roles:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Operation not permitted"
            )
