import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.services.data_ingestion import DataIngestionService

async def main():
    """Main data ingestion function"""
    print("🏗️  TINSIG AI Dashboard - Data Ingestion")
    print("=" * 50)
    
    # Initialize ingestion service
    ingestion_service = DataIngestionService()
    
    print("Starting data ingestion from all sources...")
    print("This may take a few minutes depending on data volume.")
    print()
    
    try:
        # Ingest data from all sources
        results = await ingestion_service.ingest_all_sources()
        
        # Display results
        print("📊 Ingestion Results:")
        print("-" * 30)
        
        total_success = 0
        total_errors = 0
        
        for source, result in results.items():
            status_icon = "✅" if result["status"] == "success" else "❌"
            print(f"{status_icon} {source.upper()}: {result['status']}")
            
            if result["status"] == "success":
                print(f"   📈 Records processed: {result['count']}")
                total_success += result['count']
            else:
                print(f"   ⚠️  Error: {result.get('error', 'Unknown error')}")
                total_errors += 1
        
        print("-" * 30)
        print(f"📊 Summary: {total_success} total records ingested")
        
        if total_errors > 0:
            print(f"⚠️  {total_errors} source(s) had errors")
        else:
            print("🎉 All sources ingested successfully!")
        
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Data ingestion completed!")
    print("\nNext steps:")
    print("1. Check the backend logs for any warnings")
    print("2. Start the backend server: cd backend && uvicorn main:app --reload")
    print("3. Start the frontend: cd frontend && streamlit run app.py")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
