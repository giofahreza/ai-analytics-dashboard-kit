from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from agents.orchestrator import TinsigOrchestrator

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    query: str
    intent: str
    query_type: str
    sql_query: Optional[str] = None
    data: List[Dict[str, Any]]
    response: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}

# Global orchestrator instance
orchestrator = TinsigOrchestrator()

@router.post("/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process natural language query using AI agents"""
    try:
        result = await orchestrator.process_query(request.query)
        
        return QueryResponse(
            query=result["query"],
            intent=result["intent"],
            query_type=result["query_type"],
            sql_query=result.get("sql_query"),
            data=result["data"],
            response=result["response"],
            error=result.get("error"),
            metadata=result["metadata"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.post("/analyze")
async def analyze_query(request: QueryRequest):
    """Analyze query without full processing"""
    try:
        # TODO: Implement query analysis without full execution
        return {
            "query": request.query,
            "estimated_type": "table",  # Placeholder
            "complexity": "medium",
            "estimated_time": "2-5 seconds"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query analysis failed: {str(e)}")
