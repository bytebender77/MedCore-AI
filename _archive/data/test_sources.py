import json
import os
from services.clinical_trials import ClinicalTrialsService
from services.scientific_literature import ScientificLiteratureService
from services.patents import PatentsService
from services.epidemiology import EpidemiologyService
from services.drug_regulatory import DrugRegulatoryService
from services.trade_supply import TradeSupplyService
from services.drug_pricing import DrugPricingService
from services.news_intelligence import NewsIntelligenceService

def run_tests():
    results = {}
    
    print("Testing Clinical Trials...")
    ct = ClinicalTrialsService()
    results["clinical_trials_gov"] = ct.fetch_clinical_trials_gov()
    results["who_ictrp"] = ct.fetch_who_ictrp()
    results["eu_ctr"] = ct.fetch_eu_ctr()

    print("Testing Scientific Literature...")
    sl = ScientificLiteratureService()
    results["pubmed"] = sl.fetch_pubmed()
    results["openalex"] = sl.fetch_openalex()

    print("Testing Patents...")
    pt = PatentsService()
    results["uspto"] = pt.fetch_uspto()
    results["google_patents"] = pt.fetch_google_patents()
    results["epo_ops"] = pt.fetch_epo_ops()

    print("Testing Epidemiology...")
    ep = EpidemiologyService()
    results["who_gho"] = ep.fetch_who_gho()
    results["globocan"] = ep.fetch_globocan()

    print("Testing Drug Regulatory...")
    dr = DrugRegulatoryService()
    results["fda_drugs"] = dr.fetch_fda_drugs()
    results["fda_labels"] = dr.fetch_fda_labels()
    results["ema"] = dr.fetch_ema()

    print("Testing Trade...")
    ts = TradeSupplyService()
    results["un_comtrade"] = ts.fetch_un_comtrade()
    results["wits"] = ts.fetch_wits()

    print("Testing Pricing...")
    dp = DrugPricingService()
    results["cms_medicare"] = dp.fetch_cms_medicare()
    results["nppa"] = dp.fetch_nppa_india()

    print("Testing News...")
    ni = NewsIntelligenceService()
    results["google_news"] = ni.fetch_google_news_rss()
    results["gdelt"] = ni.fetch_gdelt()

    # Save results
    with open("verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n--- Extraction Summary ---")
    for source, data in results.items():
        if isinstance(data, dict) and "error" in data:
            print(f"❌ {source}: Error - {data['error']}")
        elif isinstance(data, dict) and "message" in data:
             print(f"⚠️ {source}: Placeholder - {data['message']}")
        elif isinstance(data, dict) or isinstance(data, list):
            count = len(data) if isinstance(data, list) else len(data.keys())
            # specific checks for known structures
            if source == "clinical_trials_gov" and "studies" in data:
                count = len(data["studies"])
                if count > 0:
                    print(f"   Sample: {data['studies'][0]}")
            elif source == "pubmed" and "papers" in data:
                count = len(data["papers"])
                if count > 0:
                    print(f"   Sample: {data['papers'][0]}")
            elif source == "uspto" and "patents" in data:
                count = len(data["patents"])
                if count > 0:
                    print(f"   Sample: {data['patents'][0]}")
            elif source == "un_comtrade" and "dataset" in data:
                count = len(data["dataset"])
                if count > 0:
                    print(f"   Sample: {data['dataset'][0]}")
            elif source == "who_gho" and "value" in data:
                count = len(data["value"])
                if count > 0:
                    print(f"   Sample: {data['value'][0]}")
            elif source == "fda_drugs" and "results" in data:
                count = len(data["results"])
                if count > 0:
                    print(f"   Sample: {data['results'][0]}")
            elif source == "google_news" and "articles" in data:
                count = len(data["articles"])
                if count > 0:
                    print(f"   Sample: {data['articles'][0]}")
            elif source == "cms_medicare" and isinstance(data, list):
                count = len(data)
                if count > 0:
                    print(f"   Sample: {data[0]}")
            
            elif source == "who_ictrp" and "trials" in data:
                count = len(data["trials"])
                if count > 0:
                    print(f"   Sample: {data['trials'][0]}")
            elif source == "eu_ctr" and "trials" in data:
                count = len(data["trials"])
                if count > 0:
                    print(f"   Sample: {data['trials'][0]}")
            elif source == "nppa" and "orders" in data:
                count = len(data["orders"])
                if count > 0:
                    print(f"   Sample: {data['orders'][0]}")
            elif source == "lens" and "patents" in data:
                count = len(data["patents"])
                if count > 0:
                    print(f"   Sample: {data['patents'][0]}")
            
            print(f"✅ {source}: Extracted {count} items/fields")
        else:
            print(f"❓ {source}: Unknown format")

    print("Testing The Lens...")
    pt = PatentsService()
    results["lens"] = pt.fetch_lens_patents()
    
    # Inline check for lens
    source = "lens"
    data = results["lens"]
    if "error" in data:
        print(f"❌ {source}: Error - {data['error']}")
    elif "message" in data:
        print(f"⚠️ {source}: {data['message']}")
    elif "patents" in data:
        count = len(data["patents"])
        if count > 0:
            print(f"   Sample: {data['patents'][0]}")
        print(f"✅ {source}: Extracted {count} items/fields")
    else:
        print(f"❓ {source}: Unknown format")

    print(f"\nVerification complete. Full data saved to {os.path.abspath('verification_results.json')}")

if __name__ == "__main__":
    run_tests()
