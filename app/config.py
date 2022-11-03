from pydantic import BaseSettings

class Settings(BaseSettings):
    #SQLALCHEMY_DATABASE_URL : str
    ADMIN_MAIL : str
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
    OFFICE_START : int
    OFFICE_END : int
    DATABASE_URL : str
    class Config:
        env_file = '.env'

setting = Settings()
