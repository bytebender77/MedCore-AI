import asyncio
import os
from app.services.trade_service import TradeService
from app.core.config import get_settings
from dotenv import load_dotenv

async def test_trade_real():
    print("--- Testing Real UN Comtrade API ---")
    load_dotenv()
    
    # Force settings to real for this test
    os.environ["DATA_MODE"] = "real"
    # Ensure key is loaded (it might need reload if using pydantic settings cached, 
    # but instantiating service usually re-reads or we can patch it)
    
    service = TradeService()
    # Manually override settings if needed, but let's try default first
    service.settings.DATA_MODE = "real"
    
    # Check if key is present
    key = os.getenv("UN_COMTRADE_SUBSCRIPTION_KEY")
    print(f"Key present: {bool(key)}")
    
    query = "Medicaments"
    print(f"Fetching trade data for: {query} (HS Code 3004)")
    
    result = await service.get_trade_data(query)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        data = result.get("dataset", [])
        print(f"Success! Retrieved {len(data)} records.")
        if data:
            print(f"Sample: {data[0]}")

if __name__ == "__main__":
    asyncio.run(test_trade_real())
