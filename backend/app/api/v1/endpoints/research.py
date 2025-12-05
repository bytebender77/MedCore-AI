from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ....services.research_service import ResearchService
from ....services.report_service import ReportService

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str
    sources: Optional[List[str]] = None

@router.post("/search")
async def search_research_data(request: ResearchRequest):
    """
    Search for pharmaceutical data across multiple sources.
    Sources: clinical_trials, patents, literature, regulatory, pricing, epidemiology, news, trade.
    """
    service = ResearchService()
    try:
        results = await service.search_all(request.query, request.sources)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/report")
async def generate_report(request: ResearchRequest):
    """
    Generate an Executive Summary Report for the given query.
    Aggregates data from all sources and uses LLM to synthesize a professional report.
    """
    research_service = ResearchService()
    report_service = ReportService()
    try:
        # 1. Fetch Data
        data = await research_service.search_all(request.query, request.sources)
        
        # 2. Check for Real Data Presence (Guardrail)
        # If critical real data sources are empty, we should flag it or potentially block.
        # For now, we pass the data to ReportService, but ReportService should also be aware.
        # However, the user asked to "Block report generation when REAL data is missing" or similar.
        # Let's check if we have at least some data.
        
        has_data = False
        for key, value in data.items():
            if isinstance(value, list) and value:
                has_data = True
                break
            if isinstance(value, dict) and "error" not in value and "message" not in value:
                 # Check if dict has substantial keys
                 if any(k for k in value if k not in ["note", "source"]):
                     has_data = True
                     break
        
        if not has_data:
             return {"report": "# REAL DATA UNAVAILABLE – MOCK MODE ACTIVE\n\nNo real data could be fetched from live APIs. Report generation aborted to prevent hallucination."}

        # 3. Generate Report
        report = await report_service.generate_executive_report(request.query, data)
        
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
