from fastapi import HTTPException, status
from app.likes import schemas
from app.likes.models import Like
from app.users.models import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def like_post(
    like: schemas.LikeBase,
    db: Session,
    current_user: User,
) -> schemas.LikeBase:
    post_id, liked = like.post_id, like.liked
    old_like = (
        db.query(Like)
        .filter(Like.user_id == current_user.id, Like.post_id == post_id)
        .first()
    )

    if old_like and liked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already liked this post",
        )
    elif old_like and not liked:
        db.delete(old_like)
        db.commit()
        return like
    elif not old_like and not liked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already disliked this post",
        )
    else:
        try:
            db.add(Like(user_id=current_user.id, post_id=post_id))
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating like: {e}",
            )
        return like
