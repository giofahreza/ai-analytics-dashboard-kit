import asyncio
import asyncpg
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.database.models import Base
from backend.config import settings

async def create_database():
    """Create database and enable PostGIS extension"""
    
    print("Setting up database...")
    
    try:
        # Connect to postgres database to create our database
        conn = await asyncpg.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database='postgres'
        )
        
        try:
            # Create database if it doesn't exist
            await conn.execute(f'CREATE DATABASE {settings.DB_NAME}')
            print(f"✅ Database {settings.DB_NAME} created successfully")
        except asyncpg.DuplicateDatabaseError:
            print(f"ℹ️  Database {settings.DB_NAME} already exists")
        finally:
            await conn.close()
        
        # Connect to our database and enable PostGIS
        database_url = settings.DATABASE_URL.replace("+asyncpg", "")
        conn = await asyncpg.connect(database_url)
        
        try:
            await conn.execute('CREATE EXTENSION IF NOT EXISTS postgis')
            await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            print("✅ PostGIS and UUID extensions enabled successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not enable extensions: {e}")
        finally:
            await conn.close()
            
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")

async def create_tables():
    """Create all database tables"""
    
    print("Creating database tables...")
    
    try:
        engine = create_async_engine(settings.DATABASE_URL)
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        await engine.dispose()
        print("✅ All tables created successfully")
        
    except Exception as e:
        print(f"❌ Table creation error: {e}")

async def main():
    """Main setup function"""
    print("🏗️  TINSIG AI Dashboard - Database Setup")
    print("=" * 50)
    
    # Check if we can import required modules
    try:
        from backend.config import settings
        print(f"📍 Database URL: {settings.DATABASE_URL}")
        print(f"📍 Database Name: {settings.DB_NAME}")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the agent directory and dependencies are installed")
        return
    
    await create_database()
    await create_tables()
    
    print("\n" + "=" * 50)
    print("🎉 Database setup completed!")
    print("\nNext steps:")
    print("1. Start the source APIs (source1, source2, source3)")
    print("2. Run data ingestion: python scripts/ingest_data.py")
    print("3. Start the backend: cd backend && uvicorn main:app --reload")
    print("4. Start the frontend: cd frontend && streamlit run app.py")

if __name__ == "__main__":
    asyncio.run(main())
