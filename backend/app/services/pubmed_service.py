import aiohttp
import asyncio
from typing import List, Dict, Any
from ..core.config import get_settings
from .mock_service import MockService

class PubMedService:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    # MeSH terms mapping for common pharma queries
    MESH_MAPPINGS = {
        "respiratory infections": "Respiratory Tract Infections[MeSH]",
        "tuberculosis": "Tuberculosis[MeSH]",
        "pneumonia": "Pneumonia[MeSH]",
        "covid": "COVID-19[MeSH]",
        "asthma": "Asthma[MeSH]",
        "copd": "Pulmonary Disease, Chronic Obstructive[MeSH]",
        "cancer": "Neoplasms[MeSH]",
        "diabetes": "Diabetes Mellitus[MeSH]",
        "hypertension": "Hypertension[MeSH]",
        "malaria": "Malaria[MeSH]",
        "heart disease": "Heart Diseases[MeSH]",
        "alzheimer": "Alzheimer Disease[MeSH]"
    }
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _build_optimized_query(self, query: str, context: Dict[str, Any] = None) -> str:
        """Build an optimized PubMed query with MeSH terms"""
        query_lower = query.lower()
        
        # Check if query already contains MeSH terms
        if "[mesh]" in query_lower:
            return query
        
        # Try to find matching MeSH term
        mesh_term = None
        for keyword, mesh in self.MESH_MAPPINGS.items():
            if keyword in query_lower:
                mesh_term = mesh
                break
        
        # Build query parts
        parts = []
        
        if mesh_term:
            parts.append(mesh_term)
        else:
            # Use the query as-is but add field restrictions
            parts.append(f"({query}[Title/Abstract])")
        
        # Add therapeutic focus
        therapeutic_terms = [
            "therapeutics[MeSH]",
            "drug therapy[MeSH]", 
            "treatment outcome[MeSH]"
        ]
        parts.append(f"({' OR '.join(therapeutic_terms)})")
        
        # Add geography if specified in context
        if context and context.get("geography"):
            geo = context["geography"]
            if geo.lower() != "global":
                parts.append(f"({geo}[Affiliation] OR {geo}[Title/Abstract])")
        
        # Add recency filter (last 5 years)
        parts.append("(\"last 5 years\"[PDat])")
        
        # Exclude case reports and reviews for primary research
        # parts.append("NOT (case reports[pt] OR review[pt])")
        
        final_query = " AND ".join(parts)
        print(f"DEBUG: PubMed optimized query: {final_query}")
        return final_query
    
    async def search_papers(
        self, 
        query: str, 
        max_results: int = 10,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search PubMed using real API with optimized query.
        """
        # 1. Check Data Mode
        if self.settings.DATA_MODE != "real":
            return MockService.get_mock_pubmed_results(query)
        
        # 2. Build optimized query
        optimized_query = self._build_optimized_query(query, context)

        try:
            async with aiohttp.ClientSession(timeout=self.timeout, cookie_jar=aiohttp.DummyCookieJar()) as session:
                # Step 1: ESearch
                search_url = f"{self.BASE_URL}esearch.fcgi"
                search_params = {
                    "db": "pubmed",
                    "term": optimized_query,
                    "retmax": max_results,
                    "retmode": "json",
                    "sort": "relevance"  # Sort by relevance
                }
                if self.settings.PUBMED_API_KEY:
                    search_params["api_key"] = self.settings.PUBMED_API_KEY
                
                async with session.get(search_url, params=search_params, headers=self.headers, ssl=False) as response:
                    if response.status != 200:
                        print(f"PubMed ESearch Error: {response.status}")
                        return []
                    
                    data = await response.json()
                    id_list = data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    print(f"DEBUG: No PubMed results for query: {optimized_query}")
                    # Try simpler query as fallback
                    return await self._fallback_search(session, query, max_results)
                
                # Step 2: ESummary
                summary_url = f"{self.BASE_URL}esummary.fcgi"
                summary_params = {
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "json"
                }
                if self.settings.PUBMED_API_KEY:
                    summary_params["api_key"] = self.settings.PUBMED_API_KEY
                
                async with session.get(summary_url, params=summary_params, ssl=False) as response:
                    if response.status != 200:
                        print(f"PubMed ESummary Error: {response.status}")
                        return []
                        
                    data = await response.json()
                    results = []
                    
                    for pmid, article in data.get("result", {}).items():
                        if pmid == "uids":
                            continue
                        
                        results.append({
                            "pmid": pmid,
                            "title": article.get("title", ""),
                            "authors": [author.get("name", "") for author in article.get("authors", [])[:3]],
                            "source": article.get("source", ""),
                            "pubdate": article.get("pubdate", ""),
                            "doi": article.get("elocationid", ""),
                            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                        })
                    
                    return results

        except Exception as e:
            print(f"PubMed Service Exception: {e}")
            return []
    
    async def _fallback_search(
        self, 
        session: aiohttp.ClientSession, 
        query: str, 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Fallback to simpler query if optimized query returns no results"""
        # Extract key terms
        simple_query = query.replace("[MeSH]", "").replace("[Title/Abstract]", "")
        simple_query = " ".join(simple_query.split()[:3])  # First 3 words
        
        # Manual URL construction to avoid encoding issues
        search_url = f"{self.BASE_URL}esearch.fcgi?db=pubmed&term={simple_query.replace(' ', '+')}&retmax={max_results}&retmode=json"
        
        try:
            async with session.get(search_url, headers=self.headers, ssl=False) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                id_list = data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    return []
                
                # Fetch summaries
                summary_url = f"{self.BASE_URL}esummary.fcgi"
                summary_params = {
                    "db": "pubmed",
                    "id": ",".join(id_list),
                    "retmode": "json"
                }
                
                async with session.get(summary_url, params=summary_params, ssl=False) as resp:
                    if resp.status != 200:
                        return []
                    
                    data = await resp.json()
                    results = []
                    
                    for pmid, article in data.get("result", {}).items():
                        if pmid == "uids":
                            continue
                        
                        results.append({
                            "pmid": pmid,
                            "title": article.get("title", ""),
                            "authors": [author.get("name", "") for author in article.get("authors", [])[:3]],
                            "source": article.get("source", ""),
                            "pubdate": article.get("pubdate", ""),
                            "doi": article.get("elocationid", ""),
                            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                        })
                    
                    return results
        except:
            return []

    async def fetch_openalex(self, query: str = "biomedicine") -> Dict[str, Any]:
        """Fetches from OpenAlex API."""
        if self.settings.DATA_MODE != "real":
            return {"results": [{"id": "https://openalex.org/W123", "title": "Mock OpenAlex Paper", "publication_year": 2023}]}

        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per-page": 5,
            "filter": "is_oa:true"  # Open access only
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status != 200:
                        return {"error": f"Status {response.status}"}
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}