from xmlrpc.client import Boolean
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


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
