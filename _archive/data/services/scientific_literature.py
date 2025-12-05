import requests
import os
from typing import Dict, Any

class ScientificLiteratureService:
    def fetch_pubmed(self, term: str = "covid") -> Dict[str, Any]:
        """
        Fetches from PubMed (NCBI) E-utilities using 2-step process: ESearch -> ESummary.
        Returns: title, authors, source, pubdate, elocationid, uid.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        api_key = os.getenv("NCBI_API_KEY")
        
        # Step 1: ESearch to get IDs
        search_params = {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": 5
        }
        if api_key:
            search_params["api_key"] = api_key
            
        try:
            search_resp = requests.get(f"{base_url}esearch.fcgi", params=search_params)
            search_resp.raise_for_status()
            search_data = search_resp.json()
            
            id_list = search_data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return {"papers": []}
            
            # Step 2: ESummary to get details
            summary_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            if api_key:
                summary_params["api_key"] = api_key
                
            summary_resp = requests.get(f"{base_url}esummary.fcgi", params=summary_params)
            summary_resp.raise_for_status()
            summary_data = summary_resp.json()
            
            papers = []
            result_dict = summary_data.get("result", {})
            for uid in id_list:
                if uid in result_dict:
                    doc = result_dict[uid]
                    
                    # Extract authors
                    authors = [{"name": a.get("name")} for a in doc.get("authors", []) if "name" in a]
                    
                    papers.append({
                        "uid": uid,
                        "title": doc.get("title"),
                        "authors": authors,
                        "source": doc.get("source"),
                        "pubdate": doc.get("pubdate"),
                        "elocationid": doc.get("elocationid")
                    })
            
            return {"papers": papers}
            
        except requests.RequestException as e:
            return {"error": str(e)}

    def fetch_openalex(self, query: str = "biomedicine") -> Dict[str, Any]:
        """
        Fetches from OpenAlex API.
        """
        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per-page": 5
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
