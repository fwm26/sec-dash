from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal, init_db, ExampleData
import os
from contextlib import asynccontextmanager

# Get database credentials from environment variables (Docker will pass them)
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
server = os.getenv("DATABASE_SERVER")
database = os.getenv("DATABASE_NAME")

# Database connection URL
DATABASE_URL = f'mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+18+for+SQL+Server'

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    init_db()  # Initialize the database
    yield  # Code after yield runs during shutdown
    # Code to run on shutdown (if needed)

# Create FastAPI app with the lifespan event handler
app = FastAPI(lifespan=lifespan)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for POST data
class ExampleDataCreate(BaseModel):
    name: str
    description: str = None

# Endpoint to create new data in the database
@app.post("/data/")
def create_data(data: ExampleDataCreate, db: Session = Depends(get_db)):
    db_data = ExampleData(name=data.name, description=data.description)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
