from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, crud, models
from .database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

router = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 minutes
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Registration endpoint
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email or username already exists
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_username = crud.get_user_by_username(db, username=user.username)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    # Create user
    created_user = crud.create_user(db=db, user=user)
    return created_user

# Login endpoint
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Removed logging of plaintext password for security
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        logger.warning("Incorrect email")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not crud.verify_password(form_data.password, user.hashed_password):
        logger.warning("Incorrect password")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    logger.info(f"User {user.username} logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Logs endpoint
@router.post("/logs", response_model=schemas.LogOut, status_code=status.HTTP_201_CREATED)
def create_log_entry(log: schemas.LogCreate, db: Session = Depends(get_db)):
    return crud.create_log(db=db, log=log)

@router.get("/logs", response_model=List[schemas.LogOut])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = crud.get_logs(db, skip=skip, limit=limit)
    return logs

@router.get("/logs/{log_id}", response_model=schemas.LogOut)
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log