import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.agents.orchestrator import TinsigOrchestrator

async def test_orchestrator():
    """Test the main orchestrator with sample queries"""
    print("🤖 Testing TINSIG AI Orchestrator")
    print("=" * 40)
    
    orchestrator = TinsigOrchestrator()
    
    test_queries = [
        "How many illegal mining sites are there in Jakarta?",
        "Show me production data for this month",
        "Find mining sites near coordinates -6.2, 106.8",
        "What are the regulations about illegal mining?",
        "Show me a map of all mining activities"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 60)
        
        try:
            result = await orchestrator.process_query(query)
            
            print(f"✅ Query Type: {result['query_type']}")
            print(f"🎯 Intent: {result['intent']}")
            print(f"📊 Data Count: {len(result['data'])}")
            
            if result.get('sql_query'):
                print(f"🗃️  SQL Query: {result['sql_query']}")
            
            print(f"💬 Response: {result['response'][:200]}...")
            
            if result.get('error'):
                print(f"⚠️  Error: {result['error']}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Orchestrator testing completed!")

async def test_individual_agents():
    """Test individual agents"""
    print("\n🔧 Testing Individual Agents")
    print("=" * 40)
    
    from backend.agents.map_agent import MapAgent
    from backend.agents.table_agent import TableAgent
    from backend.agents.document_agent import DocumentAgent
    
    agents = [
        ("MapAgent", MapAgent()),
        ("TableAgent", TableAgent()),
        ("DocumentAgent", DocumentAgent())
    ]
    
    test_query = "Show me mining data"
    test_intent = "General mining query"
    
    for agent_name, agent in agents:
        print(f"\n🤖 Testing {agent_name}")
        print("-" * 30)
        
        try:
            result = await agent.process(test_query, test_intent)
            
            if result.success:
                print(f"✅ Success: {len(result.data)} data items")
                print(f"📊 Analysis: {list(result.analysis.keys())}")
            else:
                print(f"❌ Failed: {result.error}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

async def main():
    """Main testing function"""
    print("🧪 TINSIG AI Dashboard - Agent Testing")
    print("=" * 50)
    
    await test_orchestrator()
    await test_individual_agents()
    
    print("\n" + "=" * 50)
    print("🏁 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
