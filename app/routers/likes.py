from fastapi import HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LikeBase)
def create_like(
    like: schemas.LikeBase,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post_id, liked = like.post_id, like.liked
    old_like = (
        db.query(models.Like)
        .filter(models.Like.user_id == current_user.id, models.Like.post_id == post_id)
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
            db.add(models.Like(user_id=current_user.id, post_id=post_id))
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating like: {e}",
            )
        return like
