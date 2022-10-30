from re import I
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, ForeignKey,Integer,String,Boolean,Float, false, true



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    otp = Column(Integer,nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    otp = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Washes(Base):
    __tablename__ = "washes"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time_req = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    

class BookWashes(Base):
    __tablename__ = "bookwashes"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    wash_id = Column(Integer, ForeignKey(
        "washes.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=False), nullable=False)
    end_time = Column(TIMESTAMP(timezone=false), nullable=False)
    created_at = Column(TIMESTAMP(timezone=false),
                        nullable=False, server_default=text('now()'))
    completed = Column(Boolean, server_default='FALSE', nullable=False)
