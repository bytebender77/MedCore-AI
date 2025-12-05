import pytest
import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.report_generator import ReportGenerator

@pytest.mark.asyncio
async def test_generate_professional_report():
    generator = ReportGenerator(output_dir="backend/reports")
    
    query = "Analysis of mRNA Vaccines and Market Trends"
    
    synthesis = """# Executive Summary
    
The market for **mRNA vaccines** has seen exponential growth. Key players include Pfizer, Moderna, and BioNTech.

## Key Findings
- Rapid development timeline.
- High efficacy rates (>90%).
- Cold chain storage remains a challenge.

## Strategic Recommendations
1. Invest in cold chain infrastructure.
2. Explore therapeutic applications beyond infectious diseases (e.g., Oncology).
"""

    plan = {"intent": "Strategic Market Analysis"}
    
    agent_results = {
        "clinical_trials_agent": {
            "summary": "Clinical trials show strong pipeline.",
            "data": {
                "trials": [
                    {"nct_id": "NCT01234567", "title": "Phase 3 Study of mRNA-1273", "phase": "Phase 3", "status": "Completed"},
                    {"nct_id": "NCT09876543", "title": "Safety Study of BNT162b2", "phase": "Phase 1", "status": "Recruiting"},
                    {"nct_id": "NCT05555555", "title": "mRNA for Solid Tumors", "phase": "Phase 2", "status": "Active"}
                ]
            }
        },
        "patent_landscape_agent": {
            "analysis": "Patent landscape is dense with litigation risks.",
            "data": {
                "patents": [
                    {"patent_number": "US11223344", "title": "Lipid Nanoparticle Delivery System", "assignee": "Acme Pharma", "status": "Active"},
                    {"patent_number": "US99887766", "title": "Modified Nucleoside mRNA", "assignee": "BioTech Corp", "status": "Pending"}
                ]
            }
        },
        "market_intelligence_agent": {
            "analysis": "Global trade volume is high.",
            "data": {
                "market_data": {
                    "global_trade": {"total_imports_usd": 5000000000, "total_exports_usd": 4500000000, "trade_balance": -500000000},
                    "us_pricing": {"drug_name": "Comirnaty", "avg_price_per_unit": 20.50},
                    "india_pricing": {"drug_name": "Covaxin", "ceiling_price": "INR 1200"}
                }
            }
        }
    }
    
    print("\nGenerating Report...")
    filepath = await generator.generate_report(query, synthesis, agent_results, plan)
    print(f"Report generated at: {filepath}")
    
    assert os.path.exists(filepath)
    assert filepath.endswith(".pdf")

if __name__ == "__main__":
    asyncio.run(test_generate_professional_report())
