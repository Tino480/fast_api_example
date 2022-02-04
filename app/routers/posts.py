from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["posts"])


def post_to_dict(post):
    post_dict = post.__dict__
    post_dict["user"] = post.user.__dict__
    post_dict["likes"] = len(post.likes)
    return post_dict


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostGet])
def read_posts(
    db: Session = Depends(get_db),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )
    return list(map(post_to_dict, posts))


@router.get(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post_to_dict(post)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostGet)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post_to_dict(new_post)


@router.put(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_post_query = db.query(models.Post).filter(models.Post.id == post_id)
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


@router.patch(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def update_post_partial(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    db.delete(db_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
