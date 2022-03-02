from fastapi import status, Depends, APIRouter
from app.auth import services as auth_services
from app.likes import schemas
from app.likes import services
from app.users.models import User
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LikeBase)
def create_like(
    like: schemas.LikeBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_services.get_current_user),
):
    return services.like_post(like, db, current_user)
