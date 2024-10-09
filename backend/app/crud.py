from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import logging

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
    log_data = log.dict()
    log_data['site_url'] = str(log_data['site_url'])
    log_data['referrer'] = str(log_data['referrer'])
    # Convert timezone-aware datetime to naive datetime (UTC)
    log_data['timestamp'] = log_data['timestamp'].replace(tzinfo=None)
    
    db_log = models.Log(**log_data)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    logging.info(f"Log with ID {db_log.id} added to the database.")
    return db_log

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Log).offset(skip).limit(limit).all()

def get_log(db: Session, log_id: int):
    return db.query(models.Log).filter(models.Log.id == log_id).first()