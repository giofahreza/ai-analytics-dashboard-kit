import aiohttp
import asyncio
from typing import Dict, List, Optional, Any
import json
import streamlit as st
from datetime import datetime

class TinsigAPIClient:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.source1_url = "http://localhost:8001"  # Illegal Mining
        self.source2_url = "http://localhost:8002"  # Production
        self.source3_url = "http://localhost:8003"  # IUP
        
    async def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Make HTTP request with error handling"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, **kwargs) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        st.error(f"API request failed: {response.status}")
                        return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None
    
    async def query_ai_agent(self, user_query: str) -> Dict[str, Any]:
        """Send query to AI agent via backend"""
        url = f"{self.backend_url}/api/v1/query"
        payload = {"query": user_query}
        
        return await self._make_request("POST", url, json=payload)
    
    async def get_illegal_mining_data(self, filters: Dict = None) -> List[Dict]:
        """Fetch illegal mining data"""
        params = filters or {}
        url = f"{self.source1_url}/"
        
        result = await self._make_request("GET", url, params=params)
        return result.get("data", {}).get("data", []) if result else []
    
    async def get_production_data(self, filters: Dict = None) -> List[Dict]:
        """Fetch production data"""
        params = filters or {}
        url = f"{self.source2_url}/"
        
        result = await self._make_request("GET", url, params=params)
        return result.get("data", {}).get("data", []) if result else []
    
    async def get_iup_data(self, filters: Dict = None) -> List[Dict]:
        """Fetch IUP data"""
        params = filters or {}
        url = f"{self.source3_url}/"
        
        result = await self._make_request("GET", url, params=params)
        return result.get("data", {}).get("data", []) if result else []
    
    async def get_illegal_mining_count(self, kabupaten_filter: List[str]) -> int:
        """Get count of illegal mining sites"""
        try:
            data = await self.get_illegal_mining_data({"kabupaten": kabupaten_filter})
            return len(data)
        except:
            return 0
    
    async def get_production_total(self, kabupaten_filter: List[str]) -> float:
        """Get total production"""
        try:
            data = await self.get_production_data({"kabupaten": kabupaten_filter})
            return sum(float(item.get("produksi_ton", 0)) for item in data)
        except:
            return 0.0
    
    async def get_active_iups_count(self) -> int:
        """Get count of active IUPs"""
        try:
            data = await self.get_iup_data({"status": "active"})
            return len(data)
        except:
            return 0
    
    async def get_production_trends(self, kabupaten_filter: List[str]) -> List[Dict]:
        """Get production trends data"""
        try:
            data = await self.get_production_data({"kabupaten": kabupaten_filter})
            # Process data for trends - mock implementation
            return [
                {"date": "2024-01", "production": 150.5},
                {"date": "2024-02", "production": 165.2},
                {"date": "2024-03", "production": 142.8}
            ]
        except:
            return []
    
    async def get_mining_types_distribution(self) -> Dict[str, int]:
        """Get mining types distribution"""
        try:
            data = await self.get_illegal_mining_data()
            # Process data for distribution - mock implementation
            return {
                "Timah": 25,
                "Emas": 15,
                "Batubara": 10,
                "Pasir": 8
            }
        except:
            return {}
    
    async def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent activities"""
        try:
            # Mock implementation - combine recent data from all sources
            return [
                {
                    "timestamp": "2024-08-18 10:30:00",
                    "type": "Illegal Mining Detected",
                    "location": "Jakarta",
                    "details": "New illegal mining site detected in Jakarta area"
                },
                {
                    "timestamp": "2024-08-18 09:15:00", 
                    "type": "Production Report",
                    "location": "Bandung",
                    "details": "Monthly production report submitted"
                }
            ]
        except:
            return []
    
    async def get_map_data(self, layer: str, kabupaten: List[str]) -> Dict:
        """Get geospatial data for maps"""
        try:
            # Mock GeoJSON data
            return {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [106.845599, -6.208763]
                        },
                        "properties": {
                            "name": "Sample Mining Site",
                            "type": layer,
                            "kabupaten": "Jakarta"
                        }
                    }
                ]
            }
        except:
            return {"type": "FeatureCollection", "features": []}
    
    async def check_source_health(self, source: str) -> bool:
        """Check if source API is healthy"""
        try:
            if source == "source1":
                url = f"{self.source1_url}/"
            elif source == "source2":
                url = f"{self.source2_url}/"
            elif source == "source3":
                url = f"{self.source3_url}/"
            else:
                return False
            
            result = await self._make_request("GET", url)
            return result is not None
        except:
            return False
    
    async def trigger_data_sync(self) -> bool:
        """Trigger data synchronization"""
        try:
            # Mock implementation - would call backend sync endpoint
            await asyncio.sleep(2)  # Simulate sync time
            return True
        except:
            return False
