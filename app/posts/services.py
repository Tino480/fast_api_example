from fastapi import HTTPException, Response, status
from app.posts.models import Post
from app.users.models import User
from app.posts import schemas
from sqlalchemy.orm import Session
from typing import Optional


def post_to_dict(post: Post) -> dict:
    post_dict = post.__dict__
    post_dict["user"] = post.user.__dict__
    post_dict["likes"] = len(post.likes)
    return post_dict


def get_posts(
    db: Session,
    limit: int,
    skip: int,
    search: Optional[str] = "",
) -> list:
    posts = (
        db.query(Post)
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )
    return list(map(post_to_dict, posts))


def get_post(db: Session, post_id: int) -> dict:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post_to_dict(post)


def create_post(
    db: Session,
    post: schemas.PostCreate,
    current_user: User,
) -> dict:
    new_post = Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post_to_dict(new_post)


def update_post(
    db: Session,
    post_id: int,
    post: schemas.PostCreate,
    current_user: User,
) -> dict:
    db_post_query = db.query(Post).filter(Post.id == post_id)
    db_post = db_post_query.first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    db_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(db_post)
    return post_to_dict(db_post)


def partialy_update_post(
    db: Session,
    post_id: int,
    post: schemas.PostUpdate,
    current_user: User,
) -> dict:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    for key, value in post.dict().items():
        if value is not None:
            setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return post_to_dict(db_post)


def delete_post(
    db: Session,
    post_id: int,
    current_user: User,
) -> Response:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
