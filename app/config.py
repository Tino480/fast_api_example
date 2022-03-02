from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv(verbose=True)


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_NAME: str
    PEPPER: str

    class config:
        env_prefix = ""
        env_file = "../.env"


settings = Settings()
