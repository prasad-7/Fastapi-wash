from pydantic import BaseSettings

class Settings(BaseSettings):
    ADMIN_MAIL : str
    SQLALCHEMY_DATABASE_URL : str
    HOST : str
    DATABASE : str
    USER: str
    PASSWORD : str
    SECRET_KEY: str
    ALGORITHM : str
    ACCESS_EXPIRE_TIME_MINUTES : int
    DAYS_ACCEPTED : int
    SENDER_EMAIL : str
    SENDER_EMAIL_APP_PASSWORD : str

    class Config:
        env_file = '.env'

setting = Settings()
