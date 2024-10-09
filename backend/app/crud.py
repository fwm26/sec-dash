from sqlalchemy.orm import Session
from . import models, schemas

def create_example_data(db: Session, data: schemas.ExampleDataCreate):
    db_data = models.ExampleData(name=data.name, description=data.description)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
