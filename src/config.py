from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME :str
    MAIL_PASSWORD :str
    MAIL_FROM :str
    MAIL_PORT :int
    MAIL_SERVER :str
    MAIL_STARTTLS : bool = False
    MAIL_SSL_TLS : bool = True
    USE_CREDENTIALS: bool  = True
    VALIDATE_CERTS : bool = True
    DOMAIN:str


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()

celery_broken_url = Config.REDIS_URL
celery_result_backend = Config.REDIS_URL