from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from app import database
from app.auth import schemas
from app.users.models import User
from sqlalchemy.orm import Session
from app.config import settings
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str):
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        schemas.TokenData(**decoded_token)
        return decoded_token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    verified_token = verify_access_token(token)
    user_id = verified_token["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    return user


def hash(password):
    peppered_password = password + settings.PEPPER
    return pwd_context.hash(peppered_password)


def verify(password, hashed_password):
    peppered_password = password + settings.PEPPER
    return pwd_context.verify(peppered_password, hashed_password)


def login(db: Session, user_credentials: OAuth2PasswordRequestForm) -> schemas.Token:
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
