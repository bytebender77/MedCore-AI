from .base_agent import BaseAgent
from typing import Dict, Any
from ..services.pubmed_service import PubMedService

class WebIntelligenceAgent(BaseAgent):
    def __init__(self, llm_manager, web_scraper):
        super().__init__(
            llm_manager,
            web_scraper,
            name="Web Intelligence Agent",
            role="Scientific literature and market intelligence specialist"
        )
        self.service = PubMedService()
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search scientific literature with context-aware queries"""
        
        provider = context.get("provider", "openai") if context else "openai"
        
        # Get context from master agent decomposition
        disease = context.get("disease", "") if context else ""
        geography = context.get("geography", "") if context else ""
        intent = context.get("intent", "") if context else ""
        
        # Build optimized PubMed query
        if "[MeSH]" in task:
            # Already optimized query from master agent
            search_query = task
        else:
            # Optimize query using LLM
            query_prompt = f"""Convert this pharmaceutical research question into an optimized PubMed search query.

QUESTION: "{task}"
DISEASE CONTEXT: {disease}
GEOGRAPHY: {geography}

Rules:
1. Use MeSH terms where appropriate (e.g., "Respiratory Tract Infections[MeSH]")
2. Use Boolean operators (AND, OR, NOT)
3. Add therapeutic focus terms
4. Keep query under 150 characters

Examples:
- "Respiratory Tract Infections[MeSH] AND therapeutics[MeSH] AND India[Affiliation]"
- "Metformin[MeSH] AND Neoplasms[MeSH] AND (repurposing OR repositioning)"
- "Tuberculosis[MeSH] AND drug therapy[MeSH] AND (novel OR new)"

Return ONLY the query string, nothing else:"""

            search_query = await self.generate_response(
                query_prompt, 
                provider=provider, 
                temperature=0.1, 
                max_tokens=100
            )
            search_query = search_query.strip().replace('"', '').split('\n')[0]
        
        print(f"DEBUG: WebIntelligenceAgent query: '{search_query}'")

        # Use Service for PubMed with context
        pubmed_results = await self.service.search_papers(
            search_query, 
            max_results=10,
            context={"geography": geography}
        )
        
        # Web search for additional context
        web_results = await self.web_scraper.search_web(task, max_results=3)
        
        # Determine query type
        is_market_query = any(word in task.lower() for word in [
            'price', 'pricing', 'market', 'erosion', 'cost', 'sales', 
            'revenue', 'trends', 'commercial', 'competitive'
        ])
        
        if is_market_query:
            summary = await self._generate_market_analysis(task, pubmed_results, provider)
        else:
            summary = await self._generate_scientific_summary(
                task, disease, geography, pubmed_results, provider
            )
        
        summary = self._clean_response(summary)
        
        return self.format_output({
            "summary": summary,
            "pubmed_papers": pubmed_results,
            "web_sources": web_results,
            "total_sources": len(pubmed_results) + len(web_results),
            "key_papers": len(pubmed_results),
            "analysis_type": "market" if is_market_query else "scientific",
            "query_used": search_query
        })
    
    async def _generate_scientific_summary(
        self, 
        task: str, 
        disease: str, 
        geography: str,
        papers: list, 
        provider: str
    ) -> str:
        """Generate scientific literature summary"""
        
        if not papers:
            return f"""# Scientific Literature Analysis

## Summary
No relevant scientific papers found for "{task}". This may indicate:
- An emerging research area with limited published literature
- Need for broader search terms
- Opportunity for novel research

## Recommendations
1. Consider adjacent therapeutic areas
2. Review conference proceedings and preprints
3. Explore patent literature for unpublished research"""
        
        # Format papers for analysis
        papers_detail = []
        for i, paper in enumerate(papers[:7], 1):
            papers_detail.append(
                f"{i}. **{paper['title']}**\n"
                f"   - Authors: {', '.join(paper['authors'][:3])}\n"
                f"   - Source: {paper['source']} ({paper['pubdate']})\n"
                f"   - PMID: {paper['pmid']}"
            )
        
        papers_text = "\n\n".join(papers_detail)
        
        summary_prompt = f"""Analyze the scientific literature for: {task}

DISEASE/CONDITION FOCUS: {disease}
GEOGRAPHY: {geography}

RESEARCH PAPERS FOUND ({len(papers)} total):

{papers_text}

Provide a comprehensive analysis following this structure:

# Scientific Literature Analysis

## 1. Mechanisms of Action
[What molecular/cellular mechanisms are discussed? What pathways are involved?]

## 2. Clinical Applications  
[What diseases/conditions are these treatments targeting? What patient populations?]

## 3. Evidence Strength
[What types of studies (RCTs, observational, preclinical)? How strong is the evidence?]

## 4. Key Findings
[What are the most significant discoveries from these papers?]

## 5. Therapeutic Potential
[What is the clinical significance? What translation opportunities exist?]

Be SPECIFIC to {disease if disease else 'the condition'}. Reference the actual paper findings.
Write 300-400 words in professional scientific style.
START DIRECTLY with "# Scientific Literature Analysis" - no preamble."""
        
        return await self.generate_response(
            summary_prompt, 
            provider=provider, 
            temperature=0.4, 
            max_tokens=1200
        )
    
    async def _generate_market_analysis(
        self, 
        task: str, 
        papers: list, 
        provider: str
    ) -> str:
        """Generate market analysis summary"""
        
        summary_prompt = f"""Analyze pharmaceutical market dynamics for: {task}

AVAILABLE DATA:
- PubMed papers found: {len(papers)}
- Relevant paper: {papers[0]['title'] if papers else 'None'}

Provide professional market analysis:

# Market Intelligence Summary

## Current Market Dynamics
[Pricing trends, competitive pressures, market forces]

## Price Erosion Patterns  
[Typical erosion timelines, generic entry impact]

## Geographic Variations
[US vs Europe vs Emerging markets differences]

## Competitive Landscape
[Key players, market share dynamics]

## Key Insights
[3-4 actionable market insights]

Write 250-300 words, professional pharmaceutical market analysis style.
START DIRECTLY with "# Market Intelligence Summary" - no preamble."""
        
        return await self.generate_response(
            summary_prompt,
            provider=provider,
            temperature=0.4,
            max_tokens=1000
        )
    
    def _clean_response(self, text: str) -> str:
        """Remove conversational starts"""
        conversational = [
            "Okay. ", "Sure. ", "Alright. ", "I am ready", "I can analyze",
            "Please provide", "Based on the provided", "Here is", "Here's",
            "Certainly", "Of course"
        ]
        
        for phrase in conversational:
            if text.startswith(phrase):
                idx = text.find('#')
                if idx > 0:
                    text = text[idx:]
                else:
                    text = text[len(phrase):].strip()
                break
        
        return text