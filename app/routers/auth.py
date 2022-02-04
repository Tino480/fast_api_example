from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas
from ..database import get_db
from ..utils import verify
from sqlalchemy.orm import Session
from ..oauth2 import create_access_token

router = APIRouter(prefix="/login", tags=["authentication"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == user_credentials.username)
        .first()
    )
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
