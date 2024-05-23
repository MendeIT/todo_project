from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEBUG: str
    HOST: str
    PORT: str

    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f'sqlite:///{BASE_DIR}/{self.DB_NAME}'

    class Config:
        env_file = f'{BASE_DIR}.env'


settings = Settings()
