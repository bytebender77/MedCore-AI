import aiohttp
import asyncio
from typing import Dict, Any, List
from ..core.config import get_settings

class DrugRegulatoryService:
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def fetch_fda_drugs(self, search_term: str = "products.brand_name:aspirin") -> Dict[str, Any]:
        """
        Fetches from openFDA Drug API.
        """
        if self.settings.DATA_MODE != "real":
            return {"results": [{"application_number": "NDA000000", "sponsor_name": "Mock Pharma", "products": [{"brand_name": "Mock Aspirin", "marketing_status": "Prescription", "active_ingredients": [{"name": "ASPIRIN"}]}]}]}

        url = "https://api.fda.gov/drug/drugsfda.json"
        params = {
            "search": search_term,
            "limit": 5
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status != 200:
                        return {"error": f"Status {response.status}: {await response.text()}"}
                    
                    data = await response.json()
                    
                    results = []
                    if "results" in data:
                        for item in data["results"]:
                            products = []
                            for prod in item.get("products", []):
                                active_ingredients = [{"name": ing.get("name")} for ing in prod.get("active_ingredients", [])]
                                products.append({
                                    "brand_name": prod.get("brand_name"),
                                    "marketing_status": prod.get("marketing_status"),
                                    "active_ingredients": active_ingredients
                                })
                            
                            results.append({
                                "application_number": item.get("application_number"),
                                "sponsor_name": item.get("sponsor_name"),
                                "products": products
                            })
                    return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    async def fetch_fda_labels(self, search_term: str = "openfda.brand_name:aspirin") -> Dict[str, Any]:
        """
        Fetches from openFDA Label API.
        """
        if self.settings.DATA_MODE != "real":
             return {"results": [{"openfda": {"brand_name": ["Mock Label"]}, "effective_time": "20230101"}]}

        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": search_term,
            "limit": 5
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status != 200:
                         return {"error": f"Status {response.status}"}
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}

    async def fetch_ema(self) -> Dict[str, Any]:
        return {"message": "EMA data is available via website search. No simple public JSON API found."}
