import asyncio
from typing import Dict, Any, List
from .clinical_trials_service import ClinicalTrialsService
from .patent_service import PatentService
from .pubmed_service import PubMedService
from .drug_regulatory_service import DrugRegulatoryService
from .drug_pricing_service import DrugPricingService
from .epidemiology_service import EpidemiologyService
from .news_intelligence_service import NewsIntelligenceService
from .trade_service import TradeService

class ResearchService:
    def __init__(self):
        self.clinical_trials = ClinicalTrialsService()
        self.patents = PatentService()
        self.literature = PubMedService()
        self.regulatory = DrugRegulatoryService()
        self.pricing = DrugPricingService()
        self.epidemiology = EpidemiologyService()
        self.news = NewsIntelligenceService()
        self.trade = TradeService()

    async def search_all(self, query: str, sources: List[str] = None) -> Dict[str, Any]:
        """
        Aggregates data from multiple sources based on the query.
        """
        if not sources:
            # Default to all if not specified
            sources = [
                "clinical_trials", "patents", "literature", 
                "regulatory", "pricing", "epidemiology", "news", "trade"
            ]
        
        tasks = {}
        
        # Clinical Trials
        if "clinical_trials" in sources:
            tasks["clinical_trials"] = self.clinical_trials.search_trials(query)
            tasks["who_trials"] = self.clinical_trials.fetch_who_ictrp(query)
            tasks["eu_trials"] = self.clinical_trials.fetch_eu_ctr(query)

        # Patents
        if "patents" in sources:
            tasks["uspto_patents"] = self.patents.search_patents(query)
            tasks["lens_patents"] = self.patents.fetch_lens_patents(query)

        # Literature
        if "literature" in sources:
            tasks["pubmed_papers"] = self.literature.search_papers(query)
            tasks["openalex_papers"] = self.literature.fetch_openalex(query)

        # Regulatory
        if "regulatory" in sources:
            tasks["fda_drugs"] = self.regulatory.fetch_fda_drugs(query)
            tasks["fda_labels"] = self.regulatory.fetch_fda_labels(query)

        # Pricing
        if "pricing" in sources:
            tasks["cms_pricing"] = self.pricing.fetch_cms_medicare()
            tasks["nppa_pricing"] = self.pricing.fetch_nppa_india()

        # Epidemiology
        if "epidemiology" in sources:
            tasks["who_gho"] = self.epidemiology.fetch_who_gho()

        # News
        if "news" in sources:
            tasks["google_news"] = self.news.fetch_google_news_rss(query)
            tasks["gdelt_news"] = self.news.fetch_gdelt(query)
            
        # Trade
        if "trade" in sources:
            tasks["trade_data"] = self.trade.get_trade_data(query)

        # Execute all tasks concurrently
        results = {}
        keys = list(tasks.keys())
        coroutines = list(tasks.values())
        
        if coroutines:
            responses = await asyncio.gather(*coroutines, return_exceptions=True)
            
            for key, response in zip(keys, responses):
                if isinstance(response, Exception):
                    results[key] = {"error": str(response)}
                else:
                    results[key] = response
        
        return results
