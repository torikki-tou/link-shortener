from enum import Enum

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    WEBHOOK_URL: str


class Scenario(str, Enum):
    first = 'first'
    second = 'second'


settings = Settings()
