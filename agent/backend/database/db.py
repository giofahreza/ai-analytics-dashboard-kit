from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from database.models import Base
import asyncpg
from config import settings

class Database:
    def __init__(self):
        self.engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.ENVIRONMENT == "development"
        )
        self.async_session = async_sessionmaker(
            self.engine, 
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def init_db(self):
        """Initialize database tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def get_session(self):
        """Get async database session"""
        async with self.async_session() as session:
            yield session

# Global database instance
database = Database()

async def get_db():
    """Dependency for FastAPI to get database session"""
    async with database.async_session() as session:
        yield session

async def init_db():
    """Initialize database - called at startup"""
    await database.init_db()
