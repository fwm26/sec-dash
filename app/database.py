from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load environment variables for database credentials
username = os.getenv("DATABASE_USERNAME", "default_username")
password = os.getenv("DATABASE_PASSWORD", "default_password")
server = os.getenv("DATABASE_SERVER", "default_server.database.windows.net")
database = os.getenv("DATABASE_NAME", "default_database")

# Construct the Azure SQL connection string
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+18+for+SQL+Server"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session to connect to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Example model to store data
class ExampleData(Base):
    __tablename__ = "example_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

# Function to create database tables
def init_db():
    Base.metadata.create_all(bind=engine)