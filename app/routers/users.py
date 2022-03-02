from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import hash
from sqlalchemy.orm import Session
from typing import List
import re

router = APIRouter(prefix="/users", tags=["users"])


def get_user_dict(user):
    user_dict = user.__dict__
    user_dict["posts"] = list(map(lambda post: post.__dict__, user.posts))
    user_dict["liked_posts"] = list(map(lambda like: like.__dict__, user.liked_posts))
    return user_dict


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserGet])
def read_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return list(map(get_user_dict, users))


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserGet
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return get_user_dict(user)


def verify_password(password: str) -> bool:
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        return True
    else:
        return False


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserGet)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if verify_password(user.password):
        hashed_password = hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return get_user_dict(new_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not valid"
        )


@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserGet
)
def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_user_query = db.query(models.User).filter(models.User.id == user_id)
    if not db_user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return get_user_dict(db_user_query.first())


@router.patch(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserGet
)
def update_user_partial(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_patch = db.query(models.Post).filter(models.Post.id == user_id).first()
    if not db_patch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    for key, value in user.dict().items():
        if value is not None:
            setattr(db_patch, key, value)
    db.commit()
    db.refresh(db_patch)
    return get_user_dict(db_patch)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
