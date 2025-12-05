import asyncio
import os
import json
from app.services.clinical_trials_service import ClinicalTrialsService
from app.services.patent_service import PatentService
from app.services.pubmed_service import PubMedService
from app.services.drug_regulatory_service import DrugRegulatoryService
from app.services.drug_pricing_service import DrugPricingService
from app.services.epidemiology_service import EpidemiologyService
from app.services.news_intelligence_service import NewsIntelligenceService
from app.services.trade_service import TradeService
from app.core.config import get_settings
from dotenv import load_dotenv

async def test_all_services():
    print("--- Testing All Services in REAL Mode ---")
    load_dotenv()
    os.environ["DATA_MODE"] = "real"
    
    services = {
        "ClinicalTrials": ClinicalTrialsService(),
        "Patents": PatentService(),
        "PubMed": PubMedService(),
        "Regulatory": DrugRegulatoryService(),
        "Pricing": DrugPricingService(),
        "Epidemiology": EpidemiologyService(),
        "News": NewsIntelligenceService(),
        "Trade": TradeService()
    }
    
    # Force settings to real
    for name, service in services.items():
        service.settings.DATA_MODE = "real"

    results = {}

    # 1. Clinical Trials
    print("\n1. Testing Clinical Trials...")
    try:
        # ClinicalTrials.gov (API)
        res_ct = await services["ClinicalTrials"].search_trials("cancer")
        print(f"  ClinicalTrials.gov: {len(res_ct)} trials found")
        
        # WHO ICTRP (Scraper/Placeholder)
        res_who = await services["ClinicalTrials"].fetch_who_ictrp("cancer")
        print(f"  WHO ICTRP: {json.dumps(res_who)[:100]}...")
        
        # EU CTR (Scraper)
        res_eu = await services["ClinicalTrials"].fetch_eu_ctr("cancer")
        print(f"  EU CTR: {json.dumps(res_eu)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 2. Patents
    print("\n2. Testing Patents...")
    try:
        # USPTO (API)
        res_uspto = await services["Patents"].search_patents("vaccine")
        print(f"  USPTO: {len(res_uspto)} patents found")
        if isinstance(res_uspto, dict) and "error" in res_uspto:
             print(f"  USPTO Error: {res_uspto['error']}")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 3. PubMed
    print("\n3. Testing PubMed/Literature...")
    try:
        # PubMed (API)
        res_pubmed = await services["PubMed"].search_papers("metformin")
        print(f"  PubMed: {len(res_pubmed)} papers found")
        
        # OpenAlex (API)
        res_openalex = await services["PubMed"].fetch_openalex("metformin")
        print(f"  OpenAlex: {json.dumps(res_openalex)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 4. Regulatory
    print("\n4. Testing Regulatory...")
    try:
        # FDA Drugs (API)
        res_fda = await services["Regulatory"].fetch_fda_drugs("products.brand_name:aspirin")
        print(f"  FDA Drugs: {json.dumps(res_fda)[:100]}...")
        
        # FDA Labels (API)
        res_labels = await services["Regulatory"].fetch_fda_labels("openfda.brand_name:aspirin")
        print(f"  FDA Labels: {json.dumps(res_labels)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 5. Pricing
    print("\n5. Testing Pricing...")
    try:
        # CMS (API)
        res_cms = await services["Pricing"].fetch_cms_medicare()
        print(f"  CMS: {json.dumps(res_cms)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 6. Epidemiology
    print("\n6. Testing Epidemiology...")
    try:
        # WHO GHO (API)
        res_who_gho = await services["Epidemiology"].fetch_who_gho()
        print(f"  WHO GHO: {json.dumps(res_who_gho)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 7. News
    print("\n7. Testing News...")
    try:
        # Google News (RSS)
        res_gnews = await services["News"].fetch_google_news_rss("pharma")
        print(f"  Google News: {json.dumps(res_gnews)[:100]}...")
        
        # GDELT (API)
        res_gdelt = await services["News"].fetch_gdelt("pharma")
        print(f"  GDELT: {json.dumps(res_gdelt)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

    # 8. Trade
    print("\n8. Testing Trade...")
    try:
        # UN Comtrade (API)
        res_trade = await services["Trade"].get_trade_data("Medicaments")
        print(f"  Trade: {json.dumps(res_trade)[:100]}...")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_all_services())
