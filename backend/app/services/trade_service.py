import aiohttp
from typing import Dict, Any, List
from ..core.config import get_settings

class UNComtradeService:
    BASE_URL = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=45)
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.settings.COMTRADE_API_KEY
        }
    
    async def get_trade_data(self, query: str) -> Dict[str, Any]:
        """Fetch trade data from UN Comtrade"""
        if self.settings.DATA_MODE != "real":
            return self._get_mock_trade_data(query)
            
        try:
            # Map query to HS Code (Simplified mapping for demo)
            hs_code = self._map_query_to_hs_code(query)
            
            params = {
                "reporterCode": "842", # USA (as reporter)
                "partnerCode": "0",   # World
                "period": "2023",     # Recent year
                "cmdCode": hs_code,   # HS Code
                "flowCode": "M,X",    # Import, Export
                "motCode": "0",       # All modes of transport
                "customsCode": "C00"  # Customs procedure
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(self.BASE_URL, params=params, headers=self.headers, ssl=False) as response:
                    if response.status != 200:
                        print(f"UN Comtrade API Error: {response.status}")
                        return self._get_mock_trade_data(query)
                    
                    data = await response.json()
                    records = data.get("data", [])
                    
                    if not records:
                        return self._get_mock_trade_data(query)
                    
                    return self._process_trade_data(records, query)
                    
        except Exception as e:
            print(f"UN Comtrade Service Exception: {e}")
            return self._get_mock_trade_data(query)
    
    def _map_query_to_hs_code(self, query: str) -> str:
        """Simple mapping of drug types to HS Codes"""
        query = query.lower()
        if "vaccine" in query: return "3002"
        if "antibiotic" in query: return "3003"
        if "vitamin" in query: return "2936"
        if "hormone" in query: return "2937"
        return "3004" # Medicaments (General)
    
    def _process_trade_data(self, records: List[Dict], query: str) -> Dict[str, Any]:
        """Process raw API response"""
        imports = 0
        exports = 0
        
        for record in records:
            flow = record.get("flowCode")
            value = record.get("primaryValue", 0)
            
            if flow == "M": # Import
                imports += value
            elif flow == "X": # Export
                exports += value
                
        return {
            "source": "UN Comtrade (Real Data)",
            "hs_code": records[0].get("cmdCode") if records else "Unknown",
            "year": "2023",
            "total_imports_usd": imports,
            "total_exports_usd": exports,
            "trade_balance": exports - imports,
            "analysis": f"Global trade data for {query} shows ${exports:,.2f} in exports and ${imports:,.2f} in imports for USA in 2023."
        }

    def _get_mock_trade_data(self, query: str) -> Dict[str, Any]:
        """Fallback mock data"""
        return {
            "source": "UN Comtrade (Simulated)",
            "hs_code": "300490",
            "year": "2023",
            "total_imports_usd": 15000000000,
            "total_exports_usd": 12000000000,
            "trade_balance": -3000000000,
            "analysis": f"Simulated trade data for {query} indicates high import volume."
        }

# Alias for backward compatibility if needed
TradeService = UNComtradeService
