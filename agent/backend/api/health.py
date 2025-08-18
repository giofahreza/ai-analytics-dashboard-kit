from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    
    return HealthResponse(
        status="healthy",
        message="TINSIG AI Dashboard is running",
        timestamp=datetime.utcnow().isoformat()
    )

@router.get("/detailed")
async def detailed_health():
    """Detailed health check including services"""
    from datetime import datetime
    
    # TODO: Add checks for database, external APIs, etc.
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "healthy",
            "source1_api": "unknown",
            "source2_api": "unknown", 
            "source3_api": "unknown",
            "gemini_api": "unknown"
        }
    }
