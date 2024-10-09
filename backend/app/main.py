from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router
from fastapi.middleware.cors import CORSMiddleware

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sec-Dash API")

# CORS settings (adjust origins as needed)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://bertie.co.nz"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

# Include the router
app.include_router(router)
