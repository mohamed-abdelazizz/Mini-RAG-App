from pydantic_settings import BaseSettings
from pydantic import ByteSize
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: ByteSize
    FILE_DEFAULT_CHUNK_SIZE: ByteSize

    MONGODB_URL: str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
