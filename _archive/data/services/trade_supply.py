import requests
import os
from typing import Dict, Any

class TradeSupplyService:
    def fetch_un_comtrade(self) -> Dict[str, Any]:
        """
        Fetches from UN Comtrade API. Requires subscription key.
        Returns: dataset with Export Value (primaryValue) and Partner Country (partnerDesc).
        """
        url = "https://comtradeapi.worldbank.org/v1/get/HS"
        key = os.getenv("UN_COMTRADE_SUBSCRIPTION_KEY")
        if not key:
            return {"error": "UN_COMTRADE_SUBSCRIPTION_KEY not found in environment."}
        
        params = {
            "reporterCode": "842", # USA
            "period": "2023",
            "partnerCode": "0", # World
            "cmdCode": "3004", # Medicaments
            "flowCode": "M" # Import
        }
        headers = {"Ocp-Apim-Subscription-Key": key}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            trade_data = []
            if "data" in data:
                for record in data["data"]:
                    trade_data.append({
                        "cmdCode": record.get("cmdCode"),
                        "ptTitle": record.get("partnerDesc"), # Mapping partnerDesc to ptTitle
                        "primaryValue": record.get("primaryValue")
                    })
            
            return {"dataset": trade_data} # Renaming key to dataset as per request
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_wits(self) -> Dict[str, Any]:
        return {"message": "World Bank WITS API requires registration and complex query construction."}
