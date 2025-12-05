import pytest
import asyncio
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import get_settings
from app.core.llm_manager import LLMManager
from app.services.web_scraper import WebScraper
from app.agents.web_intelligence_agent import WebIntelligenceAgent
from app.agents.clinical_trials_agent import ClinicalTrialsAgent
from app.agents.worker_agents import PatentLandscapeAgent, MarketIntelligenceAgent, EXIMTrendsAgent

# Smart Mock LLM to return relevant search terms
class MockLLMManager:
    async def generate(self, messages, *args, **kwargs):
        prompt = str(messages)
        if "keywords" in prompt.lower() or "search" in prompt.lower():
            if "patent" in prompt.lower(): return {"content": "CRISPR"}
            if "clinical" in prompt.lower(): return {"content": "diabetes"}
            if "pubmed" in prompt.lower() or "literature" in prompt.lower(): return {"content": "mRNA vaccine"}
            return {"content": "vaccine"}
        return {"content": "Mock Analysis Result"}

@pytest.mark.asyncio
async def test_all_agents_real_data():
    settings = get_settings()
    
    # FORCE REAL MODE
    print("\n" + "="*50)
    print("🚀 STARTING REAL DATA VERIFICATION")
    print("="*50)
    
    original_mode = settings.DATA_MODE
    settings.DATA_MODE = "real"
    
    try:
        # Initialize dependencies
        llm_manager = MockLLMManager() # We care about data tools, not LLM analysis
        web_scraper = WebScraper()
        
        # 1. Test Web Intelligence (PubMed)
        print("\n🔍 Testing Web Intelligence (PubMed)...")
        web_agent = WebIntelligenceAgent(llm_manager, web_scraper)
        web_results = await web_agent.execute("mRNA vaccine", {"provider": "openai"})
        data = web_results.get("data", {})
        articles = data.get("articles", [])
        print(f"   -> Found {len(articles)} articles")
        if articles:
            print(f"   -> Sample: {articles[0].get('title')} (Source: {articles[0].get('source')})")
        else:
            print("   -> ❌ No articles found")

        # 2. Test Clinical Trials
        print("\n🔍 Testing Clinical Trials (ClinicalTrials.gov)...")
        ct_agent = ClinicalTrialsAgent(llm_manager, web_scraper)
        ct_results = await ct_agent.execute("diabetes", {"provider": "openai", "country": "United States"})
        data = ct_results.get("data", {})
        trials = data.get("trials", [])
        print(f"   -> Found {len(trials)} trials")
        if trials:
            print(f"   -> Sample: {trials[0].get('title')} (Status: {trials[0].get('status')})")
        else:
            print("   -> ❌ No trials found")

        # 3. Test Patent Landscape (The Lens)
        print("\n🔍 Testing Patent Landscape (The Lens)...")
        patent_agent = PatentLandscapeAgent(llm_manager, web_scraper)
        patent_results = await patent_agent.execute("CRISPR", {"provider": "openai"})
        data = patent_results.get("data", {})
        patents = data.get("patents", [])
        print(f"   -> Found {len(patents)} patents")
        if patents:
            first_patent = patents[0]
            print(f"   -> Sample: {first_patent.get('title')} (ID: {first_patent.get('patent_number')})")
            if "lens.org" in first_patent.get("url", ""):
                 print("   -> ✅ Verified Lens URL")
            else:
                 print("   -> ⚠️ URL does not look like Lens")
        else:
            print("   -> ❌ No patents found")

        # 4. Test Market Intelligence (Comtrade, CMS, NPPA)
        print("\n🔍 Testing Market Intelligence (Trade, Pricing)...")
        market_agent = MarketIntelligenceAgent(llm_manager, web_scraper)
        market_results = await market_agent.execute("Metformin", {"provider": "openai"})
        data = market_results.get("data", {}).get("market_data", {})
        
        # Comtrade
        trade = data.get("global_trade", {})
        print(f"   -> Trade Source: {trade.get('source', 'Unknown')}")
        
        # CMS
        cms = data.get("us_pricing", {})
        print(f"   -> US Pricing Source: {cms.get('source', 'Unknown')}")
        
        # NPPA
        nppa = data.get("india_pricing", {})
        print(f"   -> India Pricing Source: {nppa.get('source', 'Unknown')}")

        # 5. Test EXIM Trends
        print("\n🔍 Testing EXIM Trends...")
        exim_agent = EXIMTrendsAgent(llm_manager, web_scraper)
        exim_results = await exim_agent.execute("vaccine", {"provider": "openai"})
        data = exim_results.get("data", {}).get("trade_data", {})
        print(f"   -> EXIM Source: {data.get('source', 'Unknown')}")

    finally:
        settings.DATA_MODE = original_mode
        print("\n" + "="*50)
        print("🏁 VERIFICATION COMPLETE")
        print("="*50)

if __name__ == "__main__":
    asyncio.run(test_all_agents_real_data())
