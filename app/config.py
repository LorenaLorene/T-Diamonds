from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TRACR_BULK_URL: str
    BEARER_TOKEN: str
    PLATFORM_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
