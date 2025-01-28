from pydantic import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings():
    return Settings()
