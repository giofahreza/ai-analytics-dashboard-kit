import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DataIngestionService:
    """Service for ingesting data from source APIs"""
    
    def __init__(self):
        self.source1_url = settings.SOURCE1_URL  # Illegal Mining
        self.source2_url = settings.SOURCE2_URL  # Production
        self.source3_url = settings.SOURCE3_URL  # IUP
    
    async def ingest_all_sources(self) -> Dict[str, Any]:
        """Ingest data from all source APIs"""
        
        results = {
            "source1": {"status": "pending", "count": 0, "error": None},
            "source2": {"status": "pending", "count": 0, "error": None},
            "source3": {"status": "pending", "count": 0, "error": None}
        }
        
        # Run all ingestions concurrently
        tasks = [
            self._ingest_source1(),
            self._ingest_source2(),
            self._ingest_source3()
        ]
        
        ingestion_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(ingestion_results):
            source_key = f"source{i+1}"
            
            if isinstance(result, Exception):
                results[source_key]["status"] = "error"
                results[source_key]["error"] = str(result)
                logger.error(f"{source_key} ingestion failed: {result}")
            else:
                results[source_key]["status"] = "success"
                results[source_key]["count"] = len(result)
                logger.info(f"{source_key} ingestion completed: {len(result)} records")
        
        return results
    
    async def _ingest_source1(self) -> List[Dict[str, Any]]:
        """Ingest illegal mining data from source1"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.source1_url}/") as response:
                    if response.status == 200:
                        data = await response.json()
                        raw_data = data.get("data", {}).get("data", [])
                        
                        # Process and store in database
                        processed_data = await self._process_illegal_mining_data(raw_data)
                        await self._store_illegal_mining_data(processed_data)
                        
                        return processed_data
                    else:
                        raise Exception(f"Source1 API returned status {response.status}")
        except Exception as e:
            logger.error(f"Source1 ingestion error: {e}")
            raise
    
    async def _ingest_source2(self) -> List[Dict[str, Any]]:
        """Ingest production data from source2"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.source2_url}/") as response:
                    if response.status == 200:
                        data = await response.json()
                        raw_data = data.get("data", {}).get("data", [])
                        
                        # Process and store in database
                        processed_data = await self._process_production_data(raw_data)
                        await self._store_production_data(processed_data)
                        
                        return processed_data
                    else:
                        raise Exception(f"Source2 API returned status {response.status}")
        except Exception as e:
            logger.error(f"Source2 ingestion error: {e}")
            raise
    
    async def _ingest_source3(self) -> List[Dict[str, Any]]:
        """Ingest IUP data from source3"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.source3_url}/") as response:
                    if response.status == 200:
                        data = await response.json()
                        raw_data = data.get("data", {}).get("data", [])
                        
                        # Process and store in database
                        processed_data = await self._process_iup_data(raw_data)
                        await self._store_iup_data(processed_data)
                        
                        return processed_data
                    else:
                        raise Exception(f"Source3 API returned status {response.status}")
        except Exception as e:
            logger.error(f"Source3 ingestion error: {e}")
            raise
    
    async def _process_illegal_mining_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process and clean illegal mining data"""
        processed = []
        
        for item in raw_data:
            try:
                processed_item = {
                    "mobile_id": item.get("mobile_id"),
                    "kabupaten": item.get("kabupaten"),
                    "tanggal_survey": item.get("tanggal_survey"),
                    "lat": float(item.get("lat", 0)) if item.get("lat") else None,
                    "lng": float(item.get("lng", 0)) if item.get("lng") else None,
                    "nama_pemilik": item.get("nama_pemilik"),
                    "jenis_tambang": item.get("jenis_tambang"),
                    "kecamatan": item.get("kecamatan"),
                    "jumlah_pekerja": int(item.get("jumlah_pekerja", 0)) if item.get("jumlah_pekerja") else None,
                    "estimasi_produksi_hari": float(item.get("estimasi_produksi_hari", 0)) if item.get("estimasi_produksi_hari") else None
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Failed to process illegal mining record: {e}")
                continue
        
        return processed
    
    async def _process_production_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process and clean production data"""
        processed = []
        
        for item in raw_data:
            try:
                processed_item = {
                    "tanggal_produksi": item.get("tanggal_produksi"),
                    "lokasi": item.get("lokasi"),
                    "kabupaten": item.get("kabupaten"),
                    "kecamatan": item.get("kecamatan"),
                    "produksi_ton": float(item.get("produksi_ton", 0)) if item.get("produksi_ton") else None,
                    "kadar_sn": float(item.get("kadar_sn", 0)) if item.get("kadar_sn") else None,
                    "metode_tambang": item.get("metode_tambang"),
                    "operator": item.get("operator"),
                    "lat": float(item.get("lat", 0)) if item.get("lat") else None,
                    "lng": float(item.get("lng", 0)) if item.get("lng") else None
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Failed to process production record: {e}")
                continue
        
        return processed
    
    async def _process_iup_data(self, raw_data: List[Dict]) -> List[Dict]:
        """Process and clean IUP data"""
        processed = []
        
        for item in raw_data:
            try:
                processed_item = {
                    "name": item.get("name"),
                    "du": item.get("du"),
                    "daerah": item.get("daerah"),
                    "luas": float(item.get("luas", 0)) if item.get("luas") else None,
                    "no_sk": item.get("no_sk"),
                    "tgl_sk": item.get("tgl_sk"),
                    "cnc": item.get("cnc"),
                    "status": item.get("status"),
                    "lat": float(item.get("lat", 0)) if item.get("lat") else None,
                    "lng": float(item.get("lng", 0)) if item.get("lng") else None
                }
                processed.append(processed_item)
            except Exception as e:
                logger.warning(f"Failed to process IUP record: {e}")
                continue
        
        return processed
    
    async def _store_illegal_mining_data(self, data: List[Dict]) -> None:
        """Store processed illegal mining data in database"""
        # TODO: Implement actual database storage
        logger.info(f"Would store {len(data)} illegal mining records")
    
    async def _store_production_data(self, data: List[Dict]) -> None:
        """Store processed production data in database"""
        # TODO: Implement actual database storage
        logger.info(f"Would store {len(data)} production records")
    
    async def _store_iup_data(self, data: List[Dict]) -> None:
        """Store processed IUP data in database"""
        # TODO: Implement actual database storage
        logger.info(f"Would store {len(data)} IUP records")
