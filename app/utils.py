from passlib.context import CryptContext
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    peppered_password = password + settings.PEPPER
    return pwd_context.hash(peppered_password)


def verify(password, hashed_password):
    peppered_password = password + settings.PEPPER
    return pwd_context.verify(peppered_password, hashed_password)
