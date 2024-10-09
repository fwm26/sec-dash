import pyodbc
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from one level up (../)
load_dotenv(os.path.join(os.path.dirname(__file__), '../../docker.env'))


# Get database credentials from environment variables (Docker will pass them)
username = os.getenv("DATABASE_USERNAME")
password = os.getenv("DATABASE_PASSWORD")
server = os.getenv("DATABASE_SERVER")
database = os.getenv("DATABASE_NAME")
DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver=ODBC+Driver+18+for+SQL+Server"

# Print environment variables for debugging
print(f"Username: {username}, Password: {password}, Server: {server}, Database: {database}")


# Enable SQLAlchemy echo to see the SQL statements and connection details
engine = create_engine(DATABASE_URL, echo=True)


# Connection string for pyodbc
connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},1433;UID={username};PWD={password};DATABASE={database};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
