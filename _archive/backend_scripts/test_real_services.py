import asyncio
import os
from app.services.patent_service import PatentService
from app.services.trade_service import TradeService
from app.core.config import get_settings

async def test_real_services():
    print("--- Testing Real Services (Patents & Trade) ---")
    settings = get_settings()
    print(f"DATA_MODE: {settings.DATA_MODE}")
    
    # Test Patent Service
    print("\n1. Testing PatentService...")
    patent_service = PatentService()
    patents = await patent_service.search_patents("Metformin", max_results=3)
    print(f"Found {len(patents)} patents.")
    if patents:
        print(f"Sample: {patents[0]['title']} ({patents[0]['patent_number']})")
    
    # Test Trade Service
    print("\n2. Testing TradeService...")
    trade_service = TradeService()
    trade_data = await trade_service.get_trade_data("Pharmaceuticals")
    print(f"Commodity: {trade_data.get('commodity')}")
    print(f"HS Code: {trade_data.get('hs_code')}")
    print(f"Note: {trade_data.get('note')}")

if __name__ == "__main__":
    asyncio.run(test_real_services())
