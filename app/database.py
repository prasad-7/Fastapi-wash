from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting

uri = setting.DATABASE_URL

"""if uri and uri.startswith("postgres://"):
    url = uri.replace("postgres://", "postgresql://", 1)"""


database_connection = uri

#database_connection = setting.DATABASE_URL

engine = create_engine(database_connection)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) 


Base = declarative_base()

# intilazing
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()