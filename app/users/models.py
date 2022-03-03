from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    role = relationship("Role", back_populates="users")
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        onupdate=datetime.now,
    )
    posts = relationship("Post", back_populates="user")
    liked_posts = relationship("Like", back_populates="user")
