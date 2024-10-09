from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=False), server_default=func.now())
    event = Column(String(255))
    user = Column(String(255))
    ip = Column(String(45))  # Supports IPv6
    site_url = Column(String(2048))
    url = Column(String(2048))
    method = Column(String(10))
    user_agent = Column(String(512))
    referrer = Column(String(2048))
    query_string = Column(String(2048))
    remote_addr = Column(String(45))
    request_time = Column(Integer)
    extra = Column(Text)