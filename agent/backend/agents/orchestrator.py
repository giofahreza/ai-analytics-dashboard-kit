from typing import TypedDict, List, Dict, Any, Optional
import json
from agents.map_agent import MapAgent
from agents.table_agent import TableAgent
from agents.document_agent import DocumentAgent

class AgentState(TypedDict):
    user_query: str
    query_type: str  # "map", "table", "document", "hybrid"
    intent: str
    sql_query: Optional[str]
    data_results: List[Dict[str, Any]]
    analysis_results: str
    final_response: str
    error: Optional[str]
    metadata: Dict[str, Any]

class TinsigOrchestrator:
    """Main orchestrator for TINSIG AI agents using LangGraph workflow"""
    
    def __init__(self):
        # Initialize agents
        self.map_agent = MapAgent()
        self.table_agent = TableAgent()
        self.document_agent = DocumentAgent()
        
    async def process_query(self, user_query: str) -> Dict[str, Any]:
        """Main entry point for processing user queries"""
        
        # Initialize state
        state = AgentState(
            user_query=user_query,
            query_type="",
            intent="",
            sql_query=None,
            data_results=[],
            analysis_results="",
            final_response="",
            error=None,
            metadata={}
        )
        
        try:
            # Step 1: Classify intent
            await self._classify_intent(state)
            
            # Step 2: Route to appropriate agent
            await self._execute_agent(state)
            
            # Step 3: Synthesize response
            await self._synthesize_response(state)
            
            return {
                "query": state["user_query"],
                "intent": state["intent"],
                "query_type": state["query_type"],
                "sql_query": state.get("sql_query"),
                "data": state["data_results"],
                "response": state["final_response"],
                "error": state.get("error"),
                "metadata": state["metadata"]
            }
            
        except Exception as e:
            return {
                "query": user_query,
                "intent": "error",
                "query_type": "unknown",
                "sql_query": None,
                "data": [],
                "response": f"An error occurred while processing your query: {str(e)}",
                "error": str(e),
                "metadata": {}
            }
    
    async def _classify_intent(self, state: AgentState) -> None:
        """Classify user intent and determine which agent(s) to use"""
        
        query_lower = state["user_query"].lower()
        
        # Simple keyword-based classification
        # TODO: Replace with proper LLM-based classification
        
        if any(word in query_lower for word in ["map", "location", "coordinate", "spatial", "near", "distance", "area"]):
            state["query_type"] = "map"
            state["intent"] = "Geographic/spatial analysis query"
        elif any(word in query_lower for word in ["document", "regulation", "report", "policy", "rule", "law"]):
            state["query_type"] = "document"
            state["intent"] = "Document search and analysis query"
        elif any(word in query_lower for word in ["count", "total", "average", "statistics", "trend", "production", "data"]):
            state["query_type"] = "table"
            state["intent"] = "Data analysis and statistics query"
        else:
            state["query_type"] = "table"  # Default to table agent
            state["intent"] = "General data query"
    
    async def _execute_agent(self, state: AgentState) -> None:
        """Execute the appropriate agent based on query type"""
        
        try:
            if state["query_type"] == "map":
                result = await self.map_agent.process(
                    query=state["user_query"],
                    intent=state["intent"]
                )
            elif state["query_type"] == "document":
                result = await self.document_agent.process(
                    query=state["user_query"],
                    intent=state["intent"]
                )
            else:  # table or default
                result = await self.table_agent.process(
                    query=state["user_query"],
                    intent=state["intent"]
                )
            
            # Update state with results
            if result.success:
                state["data_results"] = result.data
                state["sql_query"] = result.sql_query
                state["metadata"]["agent_analysis"] = result.analysis
            else:
                state["error"] = result.error
                
        except Exception as e:
            state["error"] = f"Agent execution failed: {str(e)}"
    
    async def _synthesize_response(self, state: AgentState) -> None:
        """Synthesize final response using simple template"""
        
        if state.get("error"):
            state["final_response"] = f"I encountered an error while processing your query: {state['error']}"
            return
        
        # Simple response synthesis
        # TODO: Replace with proper LLM-based synthesis
        
        data_count = len(state["data_results"])
        query_type = state["query_type"]
        
        if data_count == 0:
            state["final_response"] = "I couldn't find any data matching your query. Please try refining your search terms."
        elif query_type == "map":
            state["final_response"] = f"I found {data_count} geographic features matching your query. The data includes spatial information about mining activities in the specified areas."
        elif query_type == "document":
            state["final_response"] = f"I found {data_count} relevant documents. These documents contain information related to your query about mining regulations and policies."
        else:  # table
            state["final_response"] = f"I found {data_count} records matching your query. The data shows mining statistics and trends based on your criteria."
        
        # Add SQL query info if available
        if state.get("sql_query"):
            state["final_response"] += f"\n\nThe query was executed using: {state['sql_query']}"
