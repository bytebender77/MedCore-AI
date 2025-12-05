import requests
from typing import Dict, Any

class DrugRegulatoryService:
    def fetch_fda_drugs(self, search_term: str = "products.brand_name:aspirin") -> Dict[str, Any]:
        """
        Fetches from openFDA Drug API.
        """
        url = "https://api.fda.gov/drug/drugsfda.json"
        params = {
            "search": search_term,
            "limit": 5
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
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
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_fda_labels(self, search_term: str = "openfda.brand_name:aspirin") -> Dict[str, Any]:
        """
        Fetches from openFDA Label API.
        """
        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": search_term,
            "limit": 5
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_ema(self) -> Dict[str, Any]:
        return {"message": "EMA data is available via website search. No simple public JSON API found."}
