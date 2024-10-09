from sqlalchemy import Column, Integer, String
from .database import Base

class ExampleData(Base):
    __tablename__ = "example_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
