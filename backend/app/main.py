from fastapi import FastAPI
from .database import init_db
from .routes import router
from contextlib import asynccontextmanager

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    init_db()  # Initialize the database
    yield  # Code after yield runs during shutdown

# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# Include the API router
app.include_router(router)
