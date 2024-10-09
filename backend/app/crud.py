from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# CRUD operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(
        timestamp=log.timestamp,
        event=log.event,
        user=log.user,
        ip=log.ip,
        site_url=log.site_url,
        url=log.url,
        method=log.method,
        user_agent=log.user_agent,
        referrer=log.referrer,
        query_string=log.query_string,
        remote_addr=log.remote_addr,
        request_time=log.request_time,
        extra=log.extra
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Log).offset(skip).limit(limit).all()

def get_log(db: Session, log_id: int):
    return db.query(models.Log).filter(models.Log.id == log_id).first()