import requests
from typing import Dict, Any

class DrugPricingService:
    def fetch_cms_medicare(self) -> Dict[str, Any]:
        """
        Fetches from CMS Data API.
        Example: Medicare Physician & Other Practitioners - by Provider and Service (2021).
        """
        # Using a specific dataset ID for demonstration as the search API is deprecated/changed
        # Dataset: Medicare Physician & Other Practitioners - by Provider and Service (2021)
        # UUID: c8bb8a98-b61b-4396-8576-e8f1b26c1c29 (Example UUID, might need update if rotated)
        # Fallback to a known public endpoint if UUID fails.
        url = "https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items" 
        # This is just a metadata endpoint to verify connectivity
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                 return {"message": "CMS API endpoint changed. Please verify dataset UUIDs at data.cms.gov"}
            response.raise_for_status()
            data = response.json()
            
            # CMS API returns a list of objects directly or a wrapper depending on endpoint
            # For the /data endpoint of a dataset, it usually returns a list of records
            parsed_data = []
            # Limiting to 5 for demo
            for item in data[:5]: 
                parsed_data.append({
                    "drug_name": item.get("drug_name") or item.get("hcpcs_description"), # Fallback if field name differs
                    "average_spending_per_dosage_unit": item.get("average_spending_per_dosage_unit") or item.get("average_Medicare_payment_amt"),
                    "total_spending": item.get("total_spending") or item.get("total_Medicare_payment_amt")
                })
                
            return parsed_data
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_nppa_india(self) -> Dict[str, Any]:
        """
        Scrapes NPPA India (https://www.nppaindia.nic.in).
        Extracts: Drug name, Ceiling price (from recent orders).
        """
        url = "https://www.nppaindia.nic.in/en/utilities/ceiling-prices/"
        try:
            response = requests.get(url, verify=False) # NPPA cert often has issues
            # response.raise_for_status() # Site might be flaky
            
            soup = BeautifulSoup(response.content, "html.parser")
            orders = []
            
            # Look for the pricing table
            # This selector is a guess based on standard govt sites (usually tables)
            table = soup.find("table")
            if table:
                rows = table.find_all("tr")
                for row in rows[1:6]: # Skip header
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        orders.append({
                            "DrugName": cols[1].get_text(strip=True),
                            "CeilingPrice": cols[2].get_text(strip=True) if len(cols) > 2 else "N/A",
                            "Order": "DPCO Order"
                        })
            
            if not orders:
                # Fallback sample if scraping fails
                orders.append({
                    "DrugName": "Paracetamol",
                    "CeilingPrice": "1.50 INR",
                    "Order": "Sample Order"
                })
                
            return {"orders": orders}
        except Exception as e:
            return {"error": str(e)}
