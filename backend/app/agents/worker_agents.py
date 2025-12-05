from .base_agent import BaseAgent
from typing import Dict, Any, List
import json
from datetime import datetime as dt


from ..services.patent_service import PatentService
from ..services.trade_service import UNComtradeService
from ..services.pricing_service import CMSMedicareService, NPPAScraper

class PatentLandscapeAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Patent Landscape Agent",
            role="IP analysis specialist"
        )
        self.service = PatentService()
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search and analyze patents"""
        
        # Optimize query for Patent Search
        query_prompt = f"""Extract the 2-3 most important technical keywords from this query for a patent database search. Return ONLY the keywords.
Query: "{task}"
Keywords:"""
        provider = context.get("provider", "openai") if context else "openai"
        search_query = await self.generate_response(query_prompt, provider=provider, temperature=0.1, max_tokens=20)
        search_query = search_query.strip().replace('"', '').replace('\n', ' ')
        print(f"DEBUG: PatentLandscapeAgent optimized query: '{search_query}'")

        # Use Service for Patents (Real or Mock)
        patents = await self.service.search_patents(search_query, max_results=10)
        
        if not patents:
            return self.format_output({
                "analysis": "Data not available from live sources. (No patents found or API error)",
                "patents": [],
                "total_patents": 0,
                "active_patents": 0,
                "pending_patents": 0
            }, output_type="table")
        
        active_count = len([p for p in patents if p.get("status") == "Active"])
        pending_count = len([p for p in patents if p.get("status") == "Pending"])
        
        patents_detail = []
        for i, patent in enumerate(patents[:5], 1):
            patents_detail.append(
                f"{i}. {patent['title']}\n"
                f"   {patent['patent_number']} | {patent['assignee']} | Status: {patent['status']}"
            )
        
        patents_text = "\n\n".join(patents_detail)
        
        analysis_prompt = f"""Patent landscape for: {task}
        
PATENTS: {len(patents)} identified
- Active: {active_count}
- Pending: {pending_count}

KEY PATENTS:
{patents_text}

Provide analysis:

# Patent Landscape Analysis

## IP Protection Status
[Current coverage strength]

## Key Patent Holders
[Major players]

## Freedom to Operate
[IP barriers and clearance]

## White Space Opportunities
[Gaps in coverage]

## Strategic Recommendations
[IP strategy suggestions]

Write 150-200 words. START with "# Patent Landscape Analysis"."""
        
        provider = context.get("provider", "openai") if context else "openai"
        analysis = await self.generate_response(analysis_prompt, provider=provider, temperature=0.5, max_tokens=900)
        analysis = analysis.strip()
        
        return self.format_output({
            "analysis": analysis,
            "patents": patents,
            "total_patents": len(patents),
            "active_patents": active_count,
            "pending_patents": pending_count
        }, output_type="table")

class MarketIntelligenceAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Market Intelligence Agent",
            role="Market intelligence specialist"
        )
        self.comtrade_service = UNComtradeService()
        self.cms_service = CMSMedicareService()
        self.nppa_service = NPPAScraper()
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch market insights from multiple sources"""
        
        # Fetch data from all sources in parallel
        # Extract drug name from task for pricing services
        drug_name = task.split()[0] # Simple extraction, can be improved
        
        comtrade_data = await self.comtrade_service.get_trade_data(task)
        cms_data = await self.cms_service.get_drug_pricing(drug_name)
        nppa_data = await self.nppa_service.get_ceiling_price(drug_name)
        
        market_data = {
            "global_trade": comtrade_data,
            "us_pricing": cms_data,
            "india_pricing": nppa_data
        }
        
        analysis_prompt = f"""Analyze pharmaceutical market data for: {task}
        
        GLOBAL TRADE (UN Comtrade):
        {json.dumps(comtrade_data, indent=2)}
        
        US PRICING (CMS Medicare):
        {json.dumps(cms_data, indent=2)}
        
        INDIA PRICING (NPPA):
        {json.dumps(nppa_data, indent=2)}
        
        Provide analysis:
        
        # Market Intelligence Report
        
        ## Global Trade Dynamics
        [Analyze import/export volumes and trade balance]
        
        ## Pricing Landscape
        [Compare US vs India pricing, affordability, and reimbursement]
        
        ## Market Opportunities
        [Arbitrage, export potential, and market entry strategies]
        
        Write 200-250 words. START with "# Market Intelligence Report"."""
        
        provider = context.get("provider", "openai") if context else "openai"
        analysis = await self.generate_response(analysis_prompt, provider=provider, temperature=0.5, max_tokens=1000)
        analysis = analysis.strip()
        
        return self.format_output({
            "analysis": analysis,
            "market_data": market_data
        }, output_type="graph")

class EXIMTrendsAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="EXIM Trends Agent",
            role="Trade analysis specialist"
        )
        self.service = UNComtradeService()
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze export-import trends"""
        # Use Service for Trade Data (Real or Mock)
        trade_data = await self.service.get_trade_data(task)
        
        if "error" in trade_data or "message" in trade_data:
             return self.format_output({
                "analysis": f"Data not available from live sources. ({trade_data.get('error') or trade_data.get('message')})",
                "trade_data": {}
            }, output_type="graph")

        return self.format_output({
            "analysis": f"# Trade Flow Analysis\n\nComprehensive import/export data for '{task}' requires subscription to trade databases (IHS Markit, Panjiva, Import Genius). Analysis would cover sourcing patterns, supply chain dynamics, and regulatory compliance across major markets.",
            "trade_data": trade_data
        }, output_type="graph")

class InternalKnowledgeAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Internal Knowledge Agent",
            role="Internal document specialist"
        )
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze internal documents"""
        documents = context.get("documents", []) if context else []
        
        if not documents:
            return self.format_output({
                "analysis": "# Internal Knowledge Base\n\nNo internal documents provided. Upload strategy documents, field reports, meeting minutes, or competitive intelligence files for analysis.",
                "documents_analyzed": 0
            })
        
        analysis_prompt = f"""Analyze internal documents for: {task}

{len(documents)} documents provided

Extract:
1. Strategic insights
2. Historical context
3. Internal perspectives
4. Action items

Write 100-150 words."""
        
        provider = context.get("provider", "openai") if context else "openai"
        analysis = await self.generate_response(analysis_prompt, provider=provider, temperature=0.5, max_tokens=700)
        
        return self.format_output({
            "analysis": analysis,
            "documents_analyzed": len(documents)
        })
