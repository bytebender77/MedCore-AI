import asyncio
import os
from app.services.research_service import ResearchService
from app.core.config import get_settings

async def test_integration():
    print("--- Testing Unified Research Service ---")
    settings = get_settings()
    print(f"DATA_MODE: {settings.DATA_MODE}")
    
    service = ResearchService()
    query = "Metformin"
    
    print(f"\nQuerying for: {query}")
    results = await service.search_all(query)
    
    print("\n--- Results Summary ---")
    for source, data in results.items():
        status = "Error" if "error" in data else "Success"
        count = 0
        if isinstance(data, dict):
            if "trials" in data: count = len(data["trials"])
            elif "patents" in data: count = len(data["patents"])
            elif "papers" in data: count = len(data["papers"])
            elif "results" in data: count = len(data["results"]) # FDA
            elif "data" in data: count = len(data["data"]) # CMS
            elif "value" in data: count = len(data["value"]) # WHO GHO
            elif "articles" in data: count = len(data["articles"]) # News
            elif "dataset" in data: count = len(data["dataset"]) # Trade
            elif isinstance(data, list): count = len(data) # Direct list return
        
        print(f"{source}: {status} (Items: {count})")
        
        # Print a sample if available
        if status == "Success" and count > 0:
            sample = None
            if "trials" in data: sample = data["trials"][0]
            elif "patents" in data: sample = data["patents"][0]
            elif "papers" in data: sample = data["papers"][0]
            elif "results" in data: sample = data["results"][0]
            elif "data" in data: sample = data["data"][0]
            elif "value" in data: sample = data["value"][0]
            elif "articles" in data: sample = data["articles"][0]
            elif isinstance(data, list): sample = data[0]
            
            if sample:
                print(f"  Sample: {str(sample)[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_integration())
