import os
from os import getenv
from pathlib import Path, PosixPath

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(Path(__file__).resolve().parent.parent / '.env')


class Settings(BaseSettings):
    USER: str = getenv('POSTGRES_USER', 'postgres')
    PASSWORD: str = getenv('POSTGRES_PASSWORD', 'postgres')
    HOST: str = getenv('DB_HOST', '127.0.0.1')
    PORT: str = getenv('DB_PORT', '5432')
    DB_NAME: str = getenv('DB_NAME')
    SECRET_KEY: str = getenv('SECRET_KEY', '12345')
    ALGORITHM: str = getenv('ALGORITHM', 'HS256')
    EXPIRE: int = int(getenv('EXPIRE', 86400))
    BASE_DIR: PosixPath = Path(__file__).resolve().parent
    FILE_PATH: str = getenv('FILE_PATH')
    SSH_PASSPHRASE: str = getenv('SSH_PASSPHRASE')
    SSH_USER: str = getenv('SSH_USER', 'root')
    DEBUG: bool = os.getenv('DEBUG', False)


settings = Settings()
