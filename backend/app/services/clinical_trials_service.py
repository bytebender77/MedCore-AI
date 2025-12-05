import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from ..core.config import get_settings
from .mock_service import MockService

class ClinicalTrialsService:
    BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)
    
    async def search_trials(
        self, 
        query: str, 
        max_results: int = 10,
        context: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search clinical trials with improved filtering.
        """
        # 1. Check Data Mode
        if self.settings.DATA_MODE != "real":
            return MockService.get_mock_clinical_trials(query)
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                # Build smart parameters
                params = {
                    "format": "json",
                    "pageSize": max_results,
                }
                
                # Use condition-specific search if context provided
                if context and context.get("condition"):
                    params["query.cond"] = context["condition"]
                else:
                    params["query.cond"] = query  # Use query as condition
                
                # Add country filter if specified
                if context and context.get("country"):
                    country = context["country"]
                    if country.lower() != "global":
                        params["query.locn"] = country
                
                # Filter by status - active and completed trials
                params["filter.overallStatus"] = "RECRUITING,ACTIVE_NOT_RECRUITING,COMPLETED,ENROLLING_BY_INVITATION"
                
                # Sort by most recent
                params["sort"] = "LastUpdatePostDate:desc"
                
                print(f"DEBUG: ClinicalTrials.gov params: {params}")
                
                async with session.get(self.BASE_URL, params=params, ssl=False) as response:
                    if response.status != 200:
                        print(f"ClinicalTrials API Error: {response.status}")
                        text = await response.text()
                        print(f"Response: {text[:500]}")
                        return []
                        
                    data = await response.json()
                    studies = data.get("studies", [])
                    
                    if not studies:
                        print(f"No trials found, trying broader search...")
                        return await self._fallback_search(session, query, max_results)
                    
                    return self._parse_studies(studies)

        except Exception as e:
            print(f"ClinicalTrials Service Exception: {e}")
            return []
    
    async def _fallback_search(
        self, 
        session: aiohttp.ClientSession, 
        query: str, 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Fallback to broader search if condition-specific fails"""
        params = {
            "query.term": query,
            "pageSize": max_results,
            "format": "json"
        }
        
        try:
            async with session.get(self.BASE_URL, params=params, ssl=False) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                studies = data.get("studies", [])
                return self._parse_studies(studies)
        except:
            return []
    
    def _parse_studies(self, studies: List[Dict]) -> List[Dict[str, Any]]:
        """Parse study data into clean format"""
        results = []
        
        for study in studies:
            protocol = study.get("protocolSection", {})
            id_module = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            design_module = protocol.get("designModule", {})
            conditions_module = protocol.get("conditionsModule", {})
            sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
            
            nct_id = id_module.get("nctId", "Unknown")
            title = id_module.get("briefTitle", "Unknown Title")
            status = status_module.get("overallStatus", "Unknown")
            
            # Get phase
            phases = design_module.get("phases", [])
            phase = phases[0] if phases else "Not Applicable"
            
            # Get conditions
            conditions = conditions_module.get("conditions", [])
            
            # Get sponsor
            lead_sponsor = sponsor_module.get("leadSponsor", {})
            sponsor = lead_sponsor.get("name", "Unknown")
            
            # Get locations
            locations_module = protocol.get("contactsLocationsModule", {})
            locations = locations_module.get("locations", [])
            countries = list(set([loc.get("country", "") for loc in locations if loc.get("country")]))
            
            results.append({
                "nct_id": nct_id,
                "title": title,
                "conditions": conditions,
                "phase": phase,
                "status": status,
                "sponsor": sponsor,
                "countries": countries[:5],  # Top 5 countries
                "url": f"https://clinicaltrials.gov/study/{nct_id}"
            })
        
        return results
    
    def analyze_trials(self, trials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trial landscape"""
        if not trials:
            return {
                "total_trials": 0,
                "phase_distribution": {},
                "status_distribution": {},
                "top_sponsors": [],
                "analysis": "No clinical trials found."
            }
        
        # Phase distribution
        phase_dist = {}
        for trial in trials:
            phase = trial.get("phase", "Unknown")
            phase_dist[phase] = phase_dist.get(phase, 0) + 1
        
        # Status distribution
        status_dist = {}
        for trial in trials:
            status = trial.get("status", "Unknown")
            status_dist[status] = status_dist.get(status, 0) + 1
        
        # Top sponsors
        sponsor_counts = {}
        for trial in trials:
            sponsor = trial.get("sponsor", "Unknown")
            sponsor_counts[sponsor] = sponsor_counts.get(sponsor, 0) + 1
        
        top_sponsors = sorted(sponsor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Generate analysis text
        recruiting = status_dist.get("RECRUITING", 0)
        completed = status_dist.get("COMPLETED", 0)
        
        analysis = f"""Clinical trial landscape shows {len(trials)} relevant studies. 
{recruiting} trials are actively recruiting and {completed} have been completed.
Phase distribution: {', '.join([f'{k}: {v}' for k, v in phase_dist.items()])}.
Top sponsor: {top_sponsors[0][0] if top_sponsors else 'N/A'} with {top_sponsors[0][1] if top_sponsors else 0} trials."""
        
        return {
            "total_trials": len(trials),
            "phase_distribution": phase_dist,
            "status_distribution": status_dist,
            "top_sponsors": top_sponsors,
            "analysis": analysis
        }

    async def fetch_who_ictrp(self, query: str = "cancer") -> Dict[str, Any]:
        """WHO ICTRP placeholder"""
        return {
            "message": "WHO ICTRP requires Selenium for ASP.NET. Using placeholder.",
            "trials": [{
                "TrialID": "Simulated-WHO-001",
                "Condition": query,
                "Intervention": "Investigational Drug",
                "Sponsor": "WHO Partner",
                "Country": "Global",
                "Status": "Recruiting"
            }]
        }

    async def fetch_eu_ctr(self, query: str = "cancer") -> Dict[str, Any]:
        """EU CTR placeholder"""
        if self.settings.DATA_MODE != "real":
            return {"trials": [{"Protocol": "EU-MOCK-001", "Product": "Mock Drug", "Sponsor": "EU Pharma", "Phase": "Phase 2"}]}
        
        return {
            "trials": [{
                "Protocol": "2023-001234-56",
                "Product": f"Investigational Drug for {query}",
                "Sponsor": "Pharma EU",
                "Phase": "Phase 3",
                "Results": "Available"
            }],
            "note": "Full EU CTR scraping requires BeautifulSoup"
        }