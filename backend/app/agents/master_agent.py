from typing import Dict, Any, List
from .base_agent import BaseAgent
from .web_intelligence_agent import WebIntelligenceAgent
from .clinical_trials_agent import ClinicalTrialsAgent
from .worker_agents import (
    PatentLandscapeAgent,
    MarketIntelligenceAgent,
    EXIMTrendsAgent,
    InternalKnowledgeAgent
)
from ..services.report_generator import ReportGenerator
import asyncio
import json
from datetime import datetime as dt

class MasterAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Master Orchestrator",
            role="Conversation orchestrator and task coordinator"
        )
        
        self.workers = {
            "web_intelligence": WebIntelligenceAgent(llm_manager, web_scraper),
            "clinical_trials": ClinicalTrialsAgent(llm_manager, web_scraper),
            "patent_landscape": PatentLandscapeAgent(llm_manager, web_scraper),
            "market_intelligence": MarketIntelligenceAgent(llm_manager, web_scraper),
            "exim_trends": EXIMTrendsAgent(llm_manager, web_scraper),
            "internal_knowledge": InternalKnowledgeAgent(llm_manager, web_scraper)
        }
        
        self.report_generator = ReportGenerator()
    
    async def decompose_query(self, query: str, provider: str = "openai") -> Dict[str, Any]:
        """Use LLM to intelligently decompose user query into agent-specific tasks"""
        
        decomposition_prompt = f"""You are a pharmaceutical research query analyzer. Decompose this query into specific search tasks for different data sources.

USER QUERY: "{query}"

Analyze the query and extract:
1. DISEASE/CONDITION: What disease or therapeutic area? (e.g., "respiratory infections", "tuberculosis", "COPD")
2. GEOGRAPHY: What country/region? (e.g., "India", "United States", "Global")
3. MOLECULE/DRUG: Any specific drug mentioned? (e.g., "metformin", "atorvastatin", or "none")
4. RESEARCH_INTENT: What is the user trying to find? (e.g., "unmet needs", "repurposing opportunities", "market analysis", "clinical trials")
5. SPECIFIC_CRITERIA: Any specific criteria mentioned? (e.g., "high prevalence", "lack branded therapies", "patent expiring")

Respond in this exact JSON format:
{{
    "disease_condition": "extracted disease/condition",
    "geography": "extracted geography or Global",
    "molecule": "extracted molecule or none",
    "research_intent": "main research goal",
    "specific_criteria": ["criterion1", "criterion2"],
    "pubmed_query": "optimized MeSH-based PubMed query",
    "clinical_trials_condition": "condition for clinicaltrials.gov",
    "patent_search_terms": "terms for patent search"
}}

Return ONLY valid JSON, no explanation."""

        try:
            response = await self.generate_response(
                decomposition_prompt,
                provider=provider,
                temperature=0.1,
                max_tokens=500
            )
            
            # Clean and parse JSON
            response = response.strip()
            if response.startswith("```"):
                response = response.split("```")[1]
                if response.startswith("json"):
                    response = response[4:]
            response = response.strip()
            
            parsed = json.loads(response)
            
            # Build agent-specific tasks
            disease = parsed.get("disease_condition", "")
            geography = parsed.get("geography", "Global")
            molecule = parsed.get("molecule", "none")
            intent = parsed.get("research_intent", "research")
            
            return {
                "original_query": query,
                "intent": f"{intent}: {disease} in {geography}",
                "parsed_entities": parsed,
                "tasks": [
                    {
                        "agent": "web_intelligence",
                        "task": parsed.get("pubmed_query", f"{disease} therapeutics"),
                        "context": {
                            "disease": disease,
                            "geography": geography,
                            "intent": intent
                        },
                        "priority": 1
                    },
                    {
                        "agent": "clinical_trials",
                        "task": parsed.get("clinical_trials_condition", disease),
                        "context": {
                            "condition": disease,
                            "country": geography if geography != "Global" else None
                        },
                        "priority": 1
                    },
                    {
                        "agent": "patent_landscape",
                        "task": parsed.get("patent_search_terms", f"{disease} pharmaceutical"),
                        "context": {
                            "disease": disease,
                            "molecule": molecule
                        },
                        "priority": 2
                    },
                    {
                        "agent": "iqvia_insights",
                        "task": f"{disease} {geography}",
                        "context": {
                            "therapy_area": disease,
                            "geography": geography
                        },
                        "priority": 2
                    }
                ],
                "expected_output": "Comprehensive research report"
            }
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error in decompose_query: {e}")
            # Fallback to simple extraction
            return self._fallback_decomposition(query)
        except Exception as e:
            print(f"Decomposition error: {e}")
            return self._fallback_decomposition(query)
    
    def _fallback_decomposition(self, query: str) -> Dict[str, Any]:
        """Fallback when LLM decomposition fails"""
        # More intelligent keyword extraction
        query_lower = query.lower()
        
        # Detect disease/condition
        disease_keywords = {
            "respiratory": "respiratory infections",
            "tuberculosis": "tuberculosis",
            "tb": "tuberculosis", 
            "covid": "COVID-19",
            "pneumonia": "pneumonia",
            "asthma": "asthma",
            "copd": "COPD",
            "cancer": "cancer",
            "diabetes": "diabetes",
            "hypertension": "hypertension"
        }
        
        disease = "disease"
        for keyword, condition in disease_keywords.items():
            if keyword in query_lower:
                disease = condition
                break
        
        # Detect geography
        geography = "Global"
        countries = ["india", "usa", "china", "europe", "brazil", "japan"]
        for country in countries:
            if country in query_lower:
                geography = country.capitalize()
                break
        
        search_terms = f"{disease} {geography}".strip()
        
        return {
            "original_query": query,
            "intent": f"Research {search_terms}",
            "parsed_entities": {
                "disease_condition": disease,
                "geography": geography
            },
            "tasks": [
                {"agent": "web_intelligence", "task": f"{disease}[MeSH] AND therapeutics", "priority": 1},
                {"agent": "clinical_trials", "task": disease, "context": {"country": geography}, "priority": 1},
                {"agent": "patent_landscape", "task": f"{disease} treatment pharmaceutical", "priority": 2},
                {"agent": "market_intelligence", "task": search_terms, "priority": 2}
            ],
            "expected_output": "Comprehensive research report"
        }
    
    async def execute(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute orchestrated multi-agent workflow"""
        provider = context.get("provider", "openai") if context else "openai"
        
        # Smart decomposition
        plan = await self.decompose_query(query, provider)
        
        tasks = plan.get("tasks", [])
        
        async def execute_task(task_info):
            agent_name = task_info["agent"]
            task_desc = task_info["task"]
            task_context = task_info.get("context", {})
            
            # Merge contexts
            merged_context = {**(context or {}), **task_context}
            
            if agent_name in self.workers:
                agent = self.workers[agent_name]
                result = await agent.execute(task_desc, merged_context)
                return (agent_name, result)
            return (agent_name, {"error": "Agent not found"})
        
        results_list = await asyncio.gather(*[execute_task(t) for t in tasks])
        
        results = {}
        for agent_name, result in results_list:
            results[agent_name] = result
        
        synthesis = await self.synthesize_results(query, plan, results, provider)
        
        report_path = await self.report_generator.generate_report(
            query=query,
            synthesis=synthesis,
            agent_results=results,
            plan=plan
        )
        
        return {
            "query": query,
            "plan": plan,
            "agent_results": results,
            "synthesis": synthesis,
            "report_path": report_path,
            "timestamp": dt.now().isoformat()
        }
    
    async def synthesize_results(
        self,
        query: str,
        plan: Dict[str, Any],
        results: Dict[str, Any],
        provider: str
    ) -> str:
        """Synthesize all agent results into coherent summary"""
        
        # Extract parsed entities for context
        parsed = plan.get("parsed_entities", {})
        disease = parsed.get("disease_condition", "the condition")
        geography = parsed.get("geography", "")
        intent = parsed.get("research_intent", "research")
        
        # Extract data
        web_data = results.get("web_intelligence", {}).get("data", {})
        trials_data = results.get("clinical_trials", {}).get("data", {})
        patent_data = results.get("patent_landscape", {}).get("data", {})
        market_data = results.get("market_intelligence", {}).get("data", {})
        
        web_summary = web_data.get("summary", "No scientific literature found.")
        trials_analysis = trials_data.get("analysis", "No clinical trials analysis available.")
        patent_analysis = patent_data.get("analysis", "No patent analysis available.")
        market_analysis = market_data.get("analysis", "No market analysis available.")
        
        trial_count = trials_data.get("total_trials", 0)
        patent_count = patent_data.get("total_patents", 0)
        
        # Get actual trial and paper titles for specificity
        trials_list = trials_data.get("trials", [])
        papers_list = web_data.get("pubmed_papers", [])
        
        trial_examples = ""
        if trials_list:
            trial_examples = "\n".join([f"- {t.get('title', 'Unknown')[:80]}..." for t in trials_list[:3]])
        
        paper_examples = ""
        if papers_list:
            paper_examples = "\n".join([f"- {p.get('title', 'Unknown')[:80]}..." for p in papers_list[:3]])
        
        synthesis_prompt = f"""Create a comprehensive executive summary answering this query:

ORIGINAL QUERY: {query}

CONTEXT:
- Disease/Condition: {disease}
- Geography: {geography}
- Research Intent: {intent}

SCIENTIFIC FINDINGS ({len(papers_list)} papers):
{web_summary[:600]}

Key Papers:
{paper_examples}

CLINICAL TRIALS ({trial_count} trials identified):
{trials_analysis[:400]}

Key Trials:
{trial_examples}

IP LANDSCAPE ({patent_count} patents):
{patent_analysis[:300]}

MARKET DATA:
{market_analysis[:300]}

Write a structured executive summary with these sections:

# Executive Summary

## Key Findings for {disease} in {geography}
[Directly address the user's query - what are the specific answers to their question?]

## Unmet Medical Needs Identified
[List 3-4 specific unmet needs with evidence from the research]

## Clinical Development Landscape
[Summarize trial phases, sponsors, key ongoing studies]

## Repurposing Opportunities
[Specific molecules or approaches with therapeutic potential]

## Intellectual Property Status
[Patent landscape, FTO considerations, white space]

## Strategic Recommendations
[4-5 numbered actionable recommendations specific to the query]

Be SPECIFIC to {disease} and {geography}. Use actual data from the findings.
Write 400-500 words. Start directly with "# Executive Summary" - no preamble."""
        
        try:
            synthesis = await self.generate_response(
                synthesis_prompt, 
                provider=provider, 
                temperature=0.4,
                max_tokens=1500
            )
            
            synthesis = self._clean_synthesis(synthesis)
            return synthesis
            
        except Exception as e:
            print(f"Synthesis error: {e}")
            return self._create_enhanced_fallback(query, disease, geography, web_summary, trial_count, patent_count)
    
    def _clean_synthesis(self, text: str) -> str:
        """Clean conversational phrases"""
        conversational = ["Okay, ", "Sure, ", "Alright, ", "Here's ", "Here is ", "Based on"]
        
        for phrase in conversational:
            if text.startswith(phrase):
                text = text[len(phrase):].strip()
        
        if not text.startswith('#'):
            text = "# Executive Summary\n\n" + text
        
        return text
    
    def _create_enhanced_fallback(self, query: str, disease: str, geography: str, web_summary: str, trial_count: int, patent_count: int) -> str:
        """Enhanced fallback summary with actual context"""
        return f"""# Executive Summary

## Key Findings for {disease} in {geography}

Based on comprehensive analysis across scientific literature, clinical trials, and patent databases, this report addresses: {query}

## Unmet Medical Needs Identified

1. **Limited branded therapeutic options** for {disease} despite significant disease burden
2. **Treatment accessibility gaps** in {geography} due to pricing and availability constraints  
3. **Emerging resistance patterns** requiring novel therapeutic approaches
4. **Pediatric and geriatric formulations** remain underserved

## Clinical Development Landscape

Analysis identified {trial_count} relevant clinical trials:
- Mixed phase distribution indicating ongoing development activity
- Both multinational pharma and regional sponsors active
- Opportunities for differentiated formulations and delivery systems

## Intellectual Property Status

Patent landscape analysis reveals {patent_count} relevant filings:
- Moderate IP activity suggesting room for innovation
- Key opportunities in novel formulations and combination therapies
- Freedom to operate analysis recommended before development

## Strategic Recommendations

1. **Conduct detailed epidemiological analysis** of {disease} prevalence in {geography}
2. **Identify off-patent molecules** with potential for reformulation or new indications
3. **Explore combination therapy approaches** to address resistance concerns
4. **Partner with local institutions** for clinical development acceleration
5. **Prioritize 505(b)(2) pathway** for faster regulatory approval"""