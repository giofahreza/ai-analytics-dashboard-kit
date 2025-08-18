from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://tinsig_user:tinsig_password@localhost:5432/tinsig_db")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "tinsig_db")
    DB_USER: str = os.getenv("DB_USER", "tinsig_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "tinsig_password")
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Source APIs
    SOURCE1_URL: str = os.getenv("SOURCE1_URL", "http://localhost:8001")
    SOURCE2_URL: str = os.getenv("SOURCE2_URL", "http://localhost:8002")
    SOURCE3_URL: str = os.getenv("SOURCE3_URL", "http://localhost:8003")
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-here")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8501", "http://localhost:3000", "http://127.0.0.1:8501"]
    
    # Vector Store
    VECTOR_STORE_TYPE: str = os.getenv("VECTOR_STORE_TYPE", "faiss")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    ANALYTICS_ENABLED: bool = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"

    class Config:
        env_file = ".env"

settings = Settings()
