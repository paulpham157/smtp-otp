from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    gmail_user: str
    gmail_pass: str
    gmail_tag: str = "INBOX"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
