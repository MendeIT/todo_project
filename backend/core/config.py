from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEBUG: bool
    UVICORN_HOST: str
    UVICORN_PORT: int
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_NAME: str
    JWT_PRIVATE_PATH: Path = BASE_DIR/"certs"/"jwt-private.pem"
    JWT_PUBLIC_PATH: Path = BASE_DIR/"certs"/"jwt-public.pem"
    JWT_ALGORITHM: str
    TOKEN_EXPIRATION_DATE_IN_MINUTES: int

    @property
    def ASYNC_DATABASE_URL(self):
        """Путь для асинхронного подключения к PostgreSQL."""
        return ("postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}@"
                f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_NAME}")

    class Config:
        env_file = f'{BASE_DIR}.env'


settings = Settings()
