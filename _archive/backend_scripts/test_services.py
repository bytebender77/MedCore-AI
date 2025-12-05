import asyncio
import os
from app.services.clinical_trials_service import ClinicalTrialsService
from app.services.pubmed_service import PubMedService
from app.core.config import get_settings

async def test_services():
    print("--- Testing Services ---")
    settings = get_settings()
    print(f"DATA_MODE: {settings.DATA_MODE}")
    
    # Test Clinical Trials
    print("\n1. Testing ClinicalTrialsService...")
    ct_service = ClinicalTrialsService()
    trials = await ct_service.search_trials("Metformin", max_results=3)
    print(f"Found {len(trials)} trials.")
    if trials:
        print(f"Sample: {trials[0]['title']} ({trials[0]['nct_id']})")
    
    # Test PubMed
    print("\n2. Testing PubMedService...")
    pubmed_service = PubMedService()
    papers = await pubmed_service.search_papers("Metformin oncology", max_results=3)
    print(f"Found {len(papers)} papers.")
    if papers:
        print(f"Sample: {papers[0]['title']} ({papers[0]['pmid']})")

if __name__ == "__main__":
    asyncio.run(test_services())
