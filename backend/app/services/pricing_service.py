import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from ..core.config import get_settings

class CMSMedicareService:
    """Fetches US Drug Pricing from CMS.gov (Public Domain)"""
    BASE_URL = "https://data.cms.gov/data-api/v1/dataset/5kdu-5m6x/data" # Example dataset ID for drug spending
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)
        
    async def get_drug_pricing(self, drug_name: str) -> Dict[str, Any]:
        if self.settings.DATA_MODE != "real":
            return self._get_mock_pricing(drug_name)
            
        try:
            # CMS API allows filtering
            params = {
                "filter[generic_name]": drug_name.upper()
            }
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(self.BASE_URL, params=params, ssl=False) as response:
                    if response.status != 200:
                        return self._get_mock_pricing(drug_name)
                    
                    data = await response.json()
                    if not data:
                        return self._get_mock_pricing(drug_name)
                    
                    # Process first result
                    record = data[0]
                    avg_spending = float(record.get("total_spending", 0)) / float(record.get("total_dosage_units", 1))
                    
                    return {
                        "source": "CMS Medicare (Real Data)",
                        "drug_name": record.get("generic_name"),
                        "avg_price_per_unit": avg_spending,
                        "total_spending": float(record.get("total_spending", 0)),
                        "beneficiaries": int(record.get("total_beneficiaries", 0)),
                        "year": "2022" # Dataset year
                    }
                    
        except Exception as e:
            print(f"CMS Service Exception: {e}")
            return self._get_mock_pricing(drug_name)
            
    def _get_mock_pricing(self, drug_name: str) -> Dict[str, Any]:
        return {
            "source": "CMS Medicare (Simulated)",
            "drug_name": drug_name.upper(),
            "avg_price_per_unit": 0.50,
            "total_spending": 50000000,
            "beneficiaries": 100000,
            "year": "2022"
        }

class NPPAScraper:
    """Scrapes Indian Drug Pricing from nppaindia.nic.in"""
    BASE_URL = "https://www.nppaindia.nic.in/en/utilities/ceiling-prices/"
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def get_ceiling_price(self, drug_name: str) -> Dict[str, Any]:
        if self.settings.DATA_MODE != "real":
            return self._get_mock_nppa(drug_name)
            
        try:
            # NPPA search is complex (often PDF), but we can try to scrape the HTML table if available
            # For this implementation, we'll try to fetch the main page and search for the drug name in the text
            # A full scraper would need to handle pagination and PDF parsing.
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(self.BASE_URL, headers=self.headers, ssl=False) as response:
                    if response.status != 200:
                        return self._get_mock_nppa(drug_name)
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Simple text search in the page content
                    # This is a basic implementation. Real NPPA data is often in PDFs.
                    # We check if the drug name appears in any table row.
                    
                    found = False
                    price = "N/A"
                    
                    for row in soup.find_all("tr"):
                        text = row.get_text().lower()
                        if drug_name.lower() in text:
                            found = True
                            # Try to extract a number from the last column
                            cols = row.find_all("td")
                            if cols:
                                price = cols[-1].get_text().strip()
                            break
                    
                    if found:
                        return {
                            "source": "NPPA India (Scraped)",
                            "drug_name": drug_name,
                            "ceiling_price": price,
                            "status": "Found in Ceiling Price List"
                        }
                    else:
                        return self._get_mock_nppa(drug_name)
                        
        except Exception as e:
            print(f"NPPA Scraper Exception: {e}")
            return self._get_mock_nppa(drug_name)

    def _get_mock_nppa(self, drug_name: str) -> Dict[str, Any]:
        return {
            "source": "NPPA India (Simulated)",
            "drug_name": drug_name,
            "ceiling_price": "INR 15.50",
            "status": "Simulated Data"
        }
