from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint to create new data
@router.post("/data/", response_model=schemas.ExampleDataCreate)
def create_data(data: schemas.ExampleDataCreate, db: Session = Depends(get_db)):
    return crud.create_example_data(db=db, data=data)
