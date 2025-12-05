import requests
from typing import Dict, Any

class EpidemiologyService:
    def fetch_who_gho(self, indicator_code: str = "WHOSIS_000001") -> Dict[str, Any]:
        """
        Fetches from WHO Global Health Observatory (GHO) OData API.
        Default indicator: Life expectancy at birth.
        """
        url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
        params = {"$filter": "SpatialDim eq 'USA'"} # Adding filter as per user request example
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            values = []
            if "value" in data:
                for item in data["value"]:
                    values.append({
                        "TimeDim": item.get("TimeDim"),
                        "SpatialDim": item.get("SpatialDim"),
                        "NumericValue": item.get("NumericValue")
                    })
            return {"value": values}
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_globocan(self) -> Dict[str, Any]:
        return {"message": "GLOBOCAN data is often available via GCO website. API access might be restricted."}
