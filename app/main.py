from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, init_db, ExampleData
from dotenv import load_dotenv
import os
from database import init_db
from contextlib import asynccontextmanager

# Define the FastAPI app
app = FastAPI()

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    init_db()  # Initialize the database
    yield  # Code after yield runs during shutdown
    # Code to run on shutdown (if needed)

# Assign the lifespan function to the FastAPI app
app = FastAPI(lifespan=lifespan)

# Load environment variables from the .env file
load_dotenv()

username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
server = os.getenv("DATABASE_SERVER")
database = os.getenv("DATABASE_NAME")

DATABASE_URL = f'mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+18+for+SQL+Server'

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model to handle POST request data
class ExampleDataCreate(BaseModel):
    name: str
    description: str = None

# Endpoint to post data and store it in the database
@app.post("/data/")
def create_data(data: ExampleDataCreate, db: Session = Depends(get_db)):
    # Create an instance of the ExampleData model
    db_data = ExampleData(name=data.name, description=data.description)
    
    # Add the new data to the session
    db.add(db_data)
    
    # Commit the transaction
    db.commit()
    
    # Refresh the instance to return the new data with its ID
    db.refresh(db_data)
    
    return db_data

