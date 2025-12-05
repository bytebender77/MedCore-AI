import aiohttp
import asyncio
from typing import Dict, Any, List
from ..core.config import get_settings

class EpidemiologyService:
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def fetch_who_gho(self, indicator_code: str = "WHOSIS_000001") -> Dict[str, Any]:
        """
        Fetches from WHO Global Health Observatory (GHO) OData API.
        Default indicator: Life expectancy at birth.
        """
        if self.settings.DATA_MODE != "real":
             return {"value": [{"TimeDim": 2023, "SpatialDim": "USA", "NumericValue": 78.5}]}

        url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
        params = {"$filter": "SpatialDim eq 'USA'"} 
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status != 200:
                        return {"error": f"Status {response.status}"}
                    
                    data = await response.json()
                    
                    values = []
                    if "value" in data:
                        for item in data["value"]:
                            values.append({
                                "TimeDim": item.get("TimeDim"),
                                "SpatialDim": item.get("SpatialDim"),
                                "NumericValue": item.get("NumericValue")
                            })
                    return {"value": values}
        except Exception as e:
            return {"error": str(e)}

    async def fetch_globocan(self) -> Dict[str, Any]:
        return {"message": "GLOBOCAN data is often available via GCO website. API access might be restricted."}
