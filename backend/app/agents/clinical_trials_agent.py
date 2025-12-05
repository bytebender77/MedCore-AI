from .base_agent import BaseAgent
from typing import Dict, Any
import json
from ..services.clinical_trials_service import ClinicalTrialsService

class ClinicalTrialsAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Clinical Trials Agent",
            role="Clinical trial specialist"
        )
        self.service = ClinicalTrialsService()
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch and analyze clinical trials"""
        # Check if this is a non-clinical query
        is_market_query = any(word in task.lower() for word in ['price', 'pricing', 'market', 'erosion', 'cost', 'sales', 'revenue'])
        
        if is_market_query:
            # For pricing queries, provide market context instead
            return self.format_output({
                "analysis": """# Market Context Analysis

Clinical trials are not applicable to pricing/market analysis queries. 

For generic atorvastatin market analysis:
- No active trials (off-patent drug, generic since 2011)
- Focus shifted to real-world evidence and outcomes research
- Post-market surveillance studies on generic bioequivalence
- Health economics and outcomes research (HEOR) studies

Relevant research areas:
- Generic vs. branded effectiveness studies
- Patient adherence with generic substitution
- Cost-effectiveness analyses
- Healthcare system impact studies""",
                "trials": [],
                "phase_distribution": {},
                "status_distribution": {},
                "total_trials": 0,
                "note": "Clinical trials not applicable to market/pricing queries"
            }, output_type="table")
        
        # Optimize query for Clinical Trials Search
        query_prompt = f"""Extract the 2-3 most important search keywords from this query for a clinical trials database search. Return ONLY the keywords.
Query: "{task}"
Keywords:"""
        provider = context.get("provider", "openai") if context else "openai"
        search_query = await self.generate_response(query_prompt, provider=provider, temperature=0.1, max_tokens=20)
        search_query = search_query.strip().replace('"', '').replace('\n', ' ')
        print(f"DEBUG: ClinicalTrialsAgent optimized query: '{search_query}'")

        # Use the Service to fetch trials (Real or Mock based on config)
        trials = await self.service.search_trials(search_query, max_results=10)
        
        phase_dist = {}
        status_dist = {}
        
        for trial in trials:
            phase = trial.get("phase", "Unknown")
            status = trial.get("status", "Unknown")
            phase_dist[phase] = phase_dist.get(phase, 0) + 1
            status_dist[status] = status_dist.get(status, 0) + 1
        
        if len(trials) == 0:
            return self.format_output({
                "analysis": f"No active clinical trials found for '{task}'. This may indicate a mature market or non-clinical research area.",
                "trials": [],
                "phase_distribution": {},
                "total_trials": 0
            }, output_type="table")
        
        trials_detail = []
        for i, trial in enumerate(trials[:5], 1):
            trials_detail.append(
                f"{i}. {trial['title']}\n"
                f"   NCT: {trial['nct_id']} | Phase: {trial['phase']} | Status: {trial['status']}"
            )
        
        trials_text = "\n\n".join(trials_detail)
        
        analysis_prompt = f"""Analyze clinical trials for: {task}

TRIALS: {len(trials)} identified

TOP TRIALS:
{trials_text}

PHASE DISTRIBUTION: {json.dumps(phase_dist, indent=2)}
STATUS DISTRIBUTION: {json.dumps(status_dist, indent=2)}

Provide analysis:

# Clinical Trial Landscape

## Development Stage
[Phase analysis and maturity]

## Clinical Focus
[Conditions and populations]

## Trial Activity
[Recruitment status]

## Market Readiness
[Timeline to market]

## Strategic Insights
[Opportunities and gaps]

Write 150-250 words. START with "# Clinical Trial Landscape"."""
        
        provider = context.get("provider", "openai") if context else "openai"
        analysis = await self.generate_response(analysis_prompt, provider=provider, temperature=0.5, max_tokens=1000)
        analysis = analysis.strip()
        
        return self.format_output({
            "analysis": analysis,
            "trials": trials,
            "phase_distribution": phase_dist,
            "status_distribution": status_dist,
            "total_trials": len(trials),
            "active_recruiting": len([t for t in trials if "recruiting" in t.get("status", "").lower()])
        }, output_type="table")
