import pytest
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.patent_service import PatentService
from app.core.config import get_settings

@pytest.mark.asyncio
async def test_lens_api():
    settings = get_settings()
    # Force REAL mode for this test
    original_mode = settings.DATA_MODE
    settings.DATA_MODE = "real"
    
    try:
        service = PatentService()
        print(f"\nTesting Lens API with Key: {settings.LENS_API_KEY[:5]}...")
        
        # Test with a common query
        results = await service.search_patents("CRISPR")
        
        print(f"Results Found: {len(results)}")
        if results:
            print(f"First Result: {results[0]}")
            assert "lens.org" in results[0].get("url", "")
        else:
            print("No results found.")
            
    finally:
        # Restore mode
        settings.DATA_MODE = original_mode

if __name__ == "__main__":
    asyncio.run(test_lens_api())
