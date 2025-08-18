from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class IllegalMining(Base):
    __tablename__ = "illegal_mining"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    mobile_id = Column(String, unique=True, nullable=False)
    kabupaten = Column(String, nullable=False, index=True)
    tanggal_survey = Column(DateTime, nullable=False)
    location_lat = Column(Float)  # Simplified location storage
    location_lng = Column(Float)
    nama_pemilik = Column(String)
    jenis_tambang = Column(String, index=True)
    kecamatan = Column(String, index=True)
    jumlah_pekerja = Column(Integer)
    estimasi_produksi_hari = Column(Float)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Production(Base):
    __tablename__ = "production"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tanggal_produksi = Column(DateTime, nullable=False)
    lokasi = Column(String, nullable=False)
    kabupaten = Column(String, nullable=False, index=True)
    kecamatan = Column(String, index=True)
    produksi_ton = Column(Float)
    kadar_sn = Column(Float)
    metode_tambang = Column(String)
    operator = Column(String)
    location_lat = Column(Float)  # Simplified location storage
    location_lng = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class IUP(Base):
    __tablename__ = "iup"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    du = Column(String, unique=True, nullable=False)
    location_lat = Column(Float)  # Simplified location storage
    location_lng = Column(Float)
    daerah = Column(String, nullable=False)
    luas = Column(Float)
    no_sk = Column(String)
    tgl_sk = Column(DateTime)
    cnc = Column(String)
    status = Column(String, index=True)
    polygon_data = Column(Text)  # Store polygon as text/JSON
    created_at = Column(DateTime, default=datetime.utcnow)
