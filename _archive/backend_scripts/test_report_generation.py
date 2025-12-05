import asyncio
import os
from app.services.report_service import ReportService
from dotenv import load_dotenv

async def test_report_generation():
    print("--- Testing Automated Report Generation ---")
    load_dotenv()
    
    # Mock Data (simulating what ResearchService would return)
    mock_data = {
        "clinical_trials": [
            {"nct_id": "NCT123456", "title": "Trial for Glioblastoma", "status": "Recruiting", "phase": "Phase 2"}
        ],
        "scientific_literature": [
            {"title": "New mechanisms in Glioblastoma", "source": "Nature", "pubdate": "2024"}
        ],
        "patents": [
            {"patent_number": "US1234567", "title": "Novel GBM Therapy", "status": "Active"}
        ],
        "regulatory": {
            "results": [{"application_number": "NDA123", "products": [{"brand_name": "Temozolomide"}]}]
        },
        "market_intelligence": {
            "market_size": "$2.5B",
            "growth": "8.5%"
        },
        "trade_supply": {
            "export_value": "$100M"
        }
    }
    
    service = ReportService()
    
    print("Generating report for 'Glioblastoma'...")
    try:
        report = await service.generate_executive_report("Glioblastoma", mock_data)
        print("\n--- Generated Report ---\n")
        print(report[:500] + "...\n(truncated)\n")
        
        if "# EXECUTIVE SUMMARY REPORT" in report and "1. EXECUTIVE OVERVIEW" in report:
            print("\n✅ SUCCESS: Report structure verified.")
        else:
            print("\n❌ FAILURE: Report structure missing.")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_report_generation())
