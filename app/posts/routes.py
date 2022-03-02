from fastapi import HTTPException, Response, status, Depends, APIRouter
from app.auth import services as auth_services
from app.posts.models import Post
from app.posts import services
from app.posts import schemas
from app.users.models import User
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostGet])
def read_posts(
    db: Session = Depends(get_db),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    return services.get_posts(db, limit, skip, search)


@router.get(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return services.get_post(db, post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostGet)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_services.get_current_user),
):
    return services.create_post(db, post, current_user)


@router.put(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_services.get_current_user),
):
    return services.update_post(db, post_id, post, current_user)


@router.patch(
    "/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostGet
)
def update_post_partial(
    post_id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_services.get_current_user),
):
    return services.partialy_update_post(db, post_id, post, current_user)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_services.get_current_user),
):
    return services.delete_post(db, post_id, current_user)
