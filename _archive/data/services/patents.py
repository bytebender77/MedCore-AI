import requests
import os
from typing import Dict, Any, List

class PatentsService:
    def fetch_uspto(self, query: str = "cancer") -> Dict[str, Any]:
        """
        Fetches from USPTO API.
        Returns: patentNumber, inventionTitle, assignee, archiveStatus, filingDate.
        """
        # Using the 'published-applications' endpoint as it's commonly used for search
        url = "https://developer.uspto.gov/ibd-api/v1/application/publications"
        params = {
            "searchText": query,
            "start": 0,
            "rows": 5
        }
        try:
            response = requests.get(url, params=params, verify=False)
            if response.status_code != 200:
                return {"error": f"Status {response.status_code}: {response.text}"}
            
            data = response.json()
            patents = []
            
            # The API structure usually returns a list of docs in 'response' -> 'docs' or similar
            # Based on common Solr-like structure often used by USPTO APIs:
            results = data.get("results", [])
            for doc in results:
                # Extract fields safely
                assignee = []
                assignees_list = doc.get("assignee", [])
                if assignees_list:
                    # USPTO API might return list of strings or objects. Handling both.
                    for a in assignees_list:
                        if isinstance(a, str):
                            assignee.append({"orgName": a})
                        elif isinstance(a, dict):
                            assignee.append({"orgName": a.get("orgName", "Unknown")})
                
                patents.append({
                    "patentNumber": doc.get("patentApplicationNumber"),
                    "inventionTitle": doc.get("inventionTitle"),
                    "assignee": assignee,
                    "archiveStatus": doc.get("archiveStatus"),
                    "filingDate": doc.get("filingDate")
                })
                
            return {"patents": patents}
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_lens_patents(self, query: str = "cancer") -> Dict[str, Any]:
        """
        Fetches from The Lens API (https://www.lens.org).
        Requires LENS_API_KEY.
        Extracts: lens_id, title, publication_date, applicants.
        """
        url = "https://api.lens.org/patent/search"
        api_key = os.getenv("LENS_API_KEY")
        if not api_key:
            return {"message": "LENS_API_KEY not found. Register at lens.org for a token."}
            
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "query": {
                "match": {
                    "title": query
                }
            },
            "size": 5
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            patents = []
            if "data" in data:
                for item in data["data"]:
                    # Extract applicants
                    applicants = []
                    for app in item.get("applicants", []):
                        applicants.append({"name": app.get("name")})
                        
                    patents.append({
                        "lens_id": item.get("lens_id"),
                        "title": item.get("biblio", {}).get("invention_title", {}).get("text"),
                        "publication_date": item.get("biblio", {}).get("publication_date"),
                        "applicants": applicants
                    })
            
            return {"patents": patents}
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_google_patents(self) -> Dict[str, Any]:
        """
        Placeholder for Google Patents.
        """
        return {"message": "Google Patents does not have a public API. Scraping required."}

    def fetch_epo_ops(self) -> Dict[str, Any]:
        """
        Placeholder for EPO OPS (European Patent Office).
        Requires OAuth 2.0 authentication.
        """
        return {"message": "EPO OPS requires OAuth 2.0. Implement auth flow in production."}
