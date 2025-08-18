from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class AgentResult(BaseModel):
    """Standard result format for all agents"""
    success: bool
    data: List[Dict[str, Any]]
    analysis: Dict[str, Any]
    sql_query: Optional[str] = None
    error: Optional[str] = None

class BaseAgent(ABC):
    """Base class for all TINSIG agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def process(self, query: str, intent: str, **kwargs) -> AgentResult:
        """Process a query and return results"""
        pass
    
    def _create_result(
        self, 
        success: bool = True,
        data: List[Dict[str, Any]] = None,
        analysis: Dict[str, Any] = None,
        sql_query: str = None,
        error: str = None
    ) -> AgentResult:
        """Helper to create standardized results"""
        return AgentResult(
            success=success,
            data=data or [],
            analysis=analysis or {},
            sql_query=sql_query,
            error=error
        )
