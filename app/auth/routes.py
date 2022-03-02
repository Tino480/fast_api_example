from fastapi import status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.auth import schemas
from app.database import get_db
from app.auth.services import login as login_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=["authentication"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_service(db, user_credentials)
