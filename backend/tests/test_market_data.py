import pytest
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import get_settings
from app.services.trade_service import UNComtradeService
from app.services.pricing_service import CMSMedicareService, NPPAScraper

@pytest.mark.asyncio
async def test_un_comtrade_service():
    service = UNComtradeService()
    # Use a common drug for testing
    data = await service.get_trade_data("vaccine")
    print(f"\nUN Comtrade Data: {data}")
    assert "source" in data
    assert "total_imports_usd" in data

@pytest.mark.asyncio
async def test_cms_medicare_service():
    service = CMSMedicareService()
    # Use a common generic
    data = await service.get_drug_pricing("metformin")
    print(f"\nCMS Medicare Data: {data}")
    assert "source" in data
    assert "avg_price_per_unit" in data

@pytest.mark.asyncio
async def test_nppa_scraper():
    service = NPPAScraper()
    # Use a common drug likely to be in India's price list
    data = await service.get_ceiling_price("paracetamol")
    print(f"\nNPPA Data: {data}")
    assert "source" in data
    assert "ceiling_price" in data

if __name__ == "__main__":
    # Manual run wrapper
    async def run_tests():
        print("Testing UN Comtrade...")
        await test_un_comtrade_service()
        print("Testing CMS Medicare...")
        await test_cms_medicare_service()
        print("Testing NPPA Scraper...")
        await test_nppa_scraper()
        print("All tests passed!")
    
    asyncio.run(run_tests())
