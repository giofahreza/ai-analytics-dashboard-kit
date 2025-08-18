from typing import Dict, List, Any
from .base_agent import BaseAgent, AgentResult
from services.llm_service import LLMService

class TableAgent(BaseAgent):
    """Agent for handling structured data queries"""
    
    def __init__(self):
        super().__init__("TableAgent")
        self.llm_service = LLMService()
    
    async def process(self, query: str, intent: str, **kwargs) -> AgentResult:
        """Process structured data queries"""
        try:
            # Generate SQL query from natural language
            sql_query = await self._generate_sql_query(query, intent)
            
            # Execute query (mock for now)
            data = await self._execute_query(sql_query)
            
            # Analyze results
            analysis = await self._analyze_results(data, query)
            
            return self._create_result(
                success=True,
                data=data,
                analysis=analysis,
                sql_query=sql_query
            )
            
        except Exception as e:
            return self._create_result(
                success=False,
                error=f"TableAgent processing failed: {str(e)}"
            )
    
    async def _generate_sql_query(self, query: str, intent: str) -> str:
        """Generate SQL query from natural language using LLM"""
        
        schema_info = """
        Available tables:
        - illegal_mining: id, mobile_id, kabupaten, tanggal_survey, location, nama_pemilik, jenis_tambang, kecamatan, jumlah_pekerja, estimasi_produksi_hari
        - production: id, tanggal_produksi, lokasi, kabupaten, kecamatan, produksi_ton, kadar_sn, metode_tambang, operator, location
        - iup: id, name, du, location, daerah, luas, no_sk, tgl_sk, cnc, status, polygon
        """
        
        prompt = f"""
        Generate a PostgreSQL query for the following request:
        Query: {query}
        Intent: {intent}
        
        Schema: {schema_info}
        
        Return only the SQL query, no explanation.
        Use proper PostgreSQL syntax and include appropriate WHERE, GROUP BY, ORDER BY clauses as needed.
        """
        
        try:
            # For now, return a mock query
            # In real implementation, this would use the LLM service
            return "SELECT kabupaten, COUNT(*) as count FROM illegal_mining GROUP BY kabupaten ORDER BY count DESC LIMIT 10;"
        except Exception as e:
            raise Exception(f"SQL generation failed: {str(e)}")
    
    async def _execute_query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        # TODO: Implement actual database execution
        # Mock data for now
        return [
            {"kabupaten": "Jakarta", "count": 15},
            {"kabupaten": "Bandung", "count": 12},
            {"kabupaten": "Surabaya", "count": 8}
        ]
    
    async def _analyze_results(self, data: List[Dict], original_query: str) -> Dict[str, Any]:
        """Analyze query results and provide insights"""
        
        if not data:
            return {"insight": "No data found for the given query"}
        
        return {
            "record_count": len(data),
            "data_type": "tabular",
            "key_columns": list(data[0].keys()) if data else [],
            "summary": f"Found {len(data)} records matching the query",
            "insights": [
                "Data shows distribution across multiple regions",
                "Jakarta has the highest count of illegal mining sites"
            ]
        }
