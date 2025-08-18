from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api import query, data, health
from database.db import init_db
from config import settings
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting TINSIG AI Dashboard...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down TINSIG AI Dashboard...")

# Create FastAPI app
app = FastAPI(
    title="TINSIG AI Dashboard API",
    description="AI-powered mining data analysis platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(query.router, prefix="/api/v1/query", tags=["query"])
app.include_router(data.router, prefix="/api/v1/data", tags=["data"])

@app.get("/")
async def root():
    return {"message": "TINSIG AI Dashboard API is running", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
