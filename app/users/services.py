from fastapi import HTTPException, Response, status
from app.auth import services as auth_services
from app.users.models import User
from app.posts.models import Post
from sqlalchemy.orm import Session
import re


def verify_password(password: str) -> bool:
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    if mat:
        return True
    else:
        return False


def get_user_dict(user: User) -> dict:
    user_dict = user.__dict__
    user_dict["posts"] = list(map(lambda post: post.__dict__, user.posts))
    user_dict["liked_posts"] = list(map(lambda like: like.__dict__, user.liked_posts))
    return user_dict


def get_users(db: Session) -> list:
    users = db.query(User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )
    return list(map(get_user_dict, users))


def get_user(db: Session, user_id: int) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return get_user_dict(user)


def create_user(db: Session, user: User) -> dict:
    if verify_password(user.password):
        hashed_password = auth_services.hash(user.password)
        user.password = hashed_password
        new_user = User(**user.dict())
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


def update_user(db: Session, user_id: int, user: User) -> dict:
    db_user_query = db.query(User).filter(User.id == user_id)
    if not db_user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return get_user_dict(db_user_query.first())


def partialy_update_user(db: Session, user_id: int, user: User) -> dict:
    db_patch = db.query(Post).filter(Post.id == user_id).first()
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


def delete_user(db: Session, user_id: int) -> Response:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
