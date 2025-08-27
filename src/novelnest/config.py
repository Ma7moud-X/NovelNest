from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algo: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()