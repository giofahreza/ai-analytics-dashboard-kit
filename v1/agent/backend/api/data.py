from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.db import get_db
from database.models import IllegalMining, Production, IUP

router = APIRouter()

@router.get("/illegal-mining")
async def get_illegal_mining(
    kabupaten: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get illegal mining data"""
    try:
        query = select(IllegalMining)
        
        if kabupaten:
            query = query.where(IllegalMining.kabupaten.ilike(f"%{kabupaten}%"))
        
        query = query.limit(limit)
        result = await db.execute(query)
        records = result.scalars().all()
        
        # Convert to dict format
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "mobile_id": record.mobile_id,
                "kabupaten": record.kabupaten,
                "location_lat": record.location_lat,
                "location_lng": record.location_lng,
                "nama_pemilik": record.nama_pemilik,
                "jenis_tambang": record.jenis_tambang,
                "kecamatan": record.kecamatan,
                "jumlah_pekerja": record.jumlah_pekerja,
                "estimasi_produksi_hari": record.estimasi_produksi_hari,
                "tanggal_survey": record.tanggal_survey.isoformat() if record.tanggal_survey else None,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })
        
        return {
            "data": data,
            "total": len(data),
            "filters": {"kabupaten": kabupaten, "limit": limit}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch illegal mining data: {str(e)}")

@router.get("/production")
async def get_production(
    kabupaten: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get production data"""
    try:
        query = select(Production)
        
        if kabupaten:
            query = query.where(Production.kabupaten.ilike(f"%{kabupaten}%"))
        
        if date_from:
            query = query.where(Production.tanggal_produksi >= date_from)
        
        if date_to:
            query = query.where(Production.tanggal_produksi <= date_to)
        
        query = query.limit(limit)
        result = await db.execute(query)
        records = result.scalars().all()
        
        # Convert to dict format
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "tanggal_produksi": record.tanggal_produksi.isoformat() if record.tanggal_produksi else None,
                "lokasi": record.lokasi,
                "kabupaten": record.kabupaten,
                "kecamatan": record.kecamatan,
                "location_lat": record.location_lat,
                "location_lng": record.location_lng,
                "produksi_ton": record.produksi_ton,
                "kadar_sn": record.kadar_sn,
                "metode_tambang": record.metode_tambang,
                "operator": record.operator,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })
        
        return {
            "data": data,
            "total": len(data),
            "filters": {
                "kabupaten": kabupaten,
                "date_from": date_from,
                "date_to": date_to,
                "limit": limit
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch production data: {str(e)}")

@router.get("/iup")
async def get_iup(
    status: Optional[str] = Query(None),
    kabupaten: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get IUP data"""
    try:
        query = select(IUP)
        
        if status:
            query = query.where(IUP.status.ilike(f"%{status}%"))
        
        if kabupaten:
            query = query.where(IUP.daerah.ilike(f"%{kabupaten}%"))
        
        query = query.limit(limit)
        result = await db.execute(query)
        records = result.scalars().all()
        
        # Convert to dict format
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "name": record.name,
                "du": record.du,
                "location_lat": record.location_lat,
                "location_lng": record.location_lng,
                "daerah": record.daerah,
                "kabupaten": record.daerah,  # Map daerah to kabupaten for consistency
                "luas": record.luas,
                "no_sk": record.no_sk,
                "tgl_sk": record.tgl_sk.isoformat() if record.tgl_sk else None,
                "cnc": record.cnc,
                "status": record.status,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })
        
        return {
            "data": data,
            "total": len(data),
            "filters": {"status": status, "kabupaten": kabupaten, "limit": limit}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch IUP data: {str(e)}")

@router.get("/stats/summary")
async def get_summary_stats(db: AsyncSession = Depends(get_db)):
    """Get summary statistics"""
    try:
        # Count illegal mining sites
        illegal_count_result = await db.execute(select(func.count(IllegalMining.id)))
        illegal_count = illegal_count_result.scalar_one()
        
        # Count active IUPs
        active_iup_result = await db.execute(
            select(func.count(IUP.id)).where(IUP.status.ilike("%active%"))
        )
        active_iup_count = active_iup_result.scalar_one()
        
        # Total production
        production_sum_result = await db.execute(select(func.sum(Production.produksi_ton)))
        total_production = production_sum_result.scalar_one() or 0.0
        
        return {
            "illegal_mining_count": illegal_count,
            "active_iup_count": active_iup_count,
            "total_production_tons": float(total_production),
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch summary stats: {str(e)}")

@router.get("/map-data")
async def get_map_data(
    layer: str = Query("all"),
    kabupaten: Optional[List[str]] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get geospatial data for maps"""
    try:
        features = []
        
        if layer in ["all", "illegal"]:
            # Get illegal mining data
            query = select(IllegalMining)
            if kabupaten:
                query = query.where(IllegalMining.kabupaten.in_(kabupaten))
            result = await db.execute(query)
            records = result.scalars().all()
            
            for record in records:
                if record.location_lat and record.location_lng:
                    features.append({
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [record.location_lng, record.location_lat]
                        },
                        "properties": {
                            "type": "illegal",
                            "id": record.id,
                            "kabupaten": record.kabupaten,
                            "jenis_tambang": record.jenis_tambang,
                            "nama_pemilik": record.nama_pemilik
                        }
                    })
        
        return {
            "type": "FeatureCollection",
            "features": features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch map data: {str(e)}")
