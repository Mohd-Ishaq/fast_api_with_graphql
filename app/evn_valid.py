from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    ALGORITHM: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_EXPIRE_TIME: int
    REFRESH_EXPIRE_MINUTES: int


setting = Settings(_env_file=".env")