from xmlrpc.client import Boolean
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    rating = Column(Integer, server_default="0", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
        onupdate=datetime.now,
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")


class User(Base):
    __tablename__ = "users"
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
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


class Like(Base):
    __tablename__ = "likes"
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="liked_posts")
