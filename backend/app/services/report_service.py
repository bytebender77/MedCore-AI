import json
from typing import Dict, Any
from ..core.config import get_settings
from ..core.llm_manager import LLMManager

class ReportService:
    def __init__(self):
        self.settings = get_settings()
        self.llm_manager = LLMManager(self.settings)

    async def generate_executive_report(self, query: str, data: Dict[str, Any]) -> str:
        """
        Generates a professional executive summary report using the LLM.
        """
        
        # 1. Prepare Data Context
        # We need to serialize the data to a string to pass to the LLM
        # We'll truncate if it's too large, but for now we assume it fits in context (GPT-4o/Turbo has large context)
        
        clinical_data = json.dumps(data.get("clinical_trials", {}), indent=2)[:5000] # Truncate to avoid context overflow if huge
        literature_data = json.dumps(data.get("scientific_literature", {}), indent=2)[:5000]
        patent_data = json.dumps(data.get("patents", {}), indent=2)[:5000]
        regulatory_data = json.dumps(data.get("regulatory", {}), indent=2)[:5000]
        market_data = json.dumps(data.get("market_intelligence", {}), indent=2)[:5000]
        trade_data = json.dumps(data.get("trade_supply", {}), indent=2)[:5000]
        
        # 2. Construct Prompt
        prompt = f"""
You are a senior pharmaceutical strategy consultant and scientific analyst.

You are provided with structured outputs from multiple specialized AI agents for the query:
"{query}"

Your task is to generate a PROFESSIONAL, BUSINESS-READY, EXECUTIVE SUMMARY REPORT
for pharma R&D, portfolio planning, and investment decision-making.

This is NOT a research paper.
This is a concise, high-impact STRATEGIC SUMMARY REPORT.

--------------------------------
DATA INPUT (FROM AGENTS)
--------------------------------

1. Clinical Trial Pipeline Data
{clinical_data}

2. Scientific & Medical Evidence
{literature_data}

3. Patent & Intellectual Property Landscape
{patent_data}

4. Market & Pricing Intelligence
{market_data}

5. Regulatory & Access Information
{regulatory_data}

6. Trade & Supply Chain Insights
{trade_data}

--------------------------------
REPORT STYLE & QUALITY RULES
--------------------------------

1. PRIORITIZE REAL DATA:
   - Treat ClinicalTrials.gov and PubMed outputs as PRIMARY EVIDENCE.
   - Clearly label any section based on SIMULATED / MOCK data.
   - Do NOT present simulated market, trade, or patent data as verified facts if the input indicates it is mock.

2. EXECUTIVE TONE:
   - Professional, concise, decision-focused.
   - No academic writing.
   - No exaggeration or marketing language.
   - Use risk-aware language: "indicates", "appears", "suggests", "preliminary".

3. LENGTH:
   - Equivalent to 1.5 to 2 pages.
   - Crisp paragraphs and compact tables.

--------------------------------
STRUCTURE THE SUMMARY REPORT EXACTLY AS FOLLOWS
--------------------------------

# EXECUTIVE SUMMARY REPORT: {query}

**Date:** (Current Date)
**Subject:** Strategic Analysis of {query}
**Prepared By:** Antigravity AI Strategy Consultant

--------------------------------
1. EXECUTIVE OVERVIEW
--------------------------------
- 6–8 line high-level summary of:
  - Disease area / Topic
  - Current development activity
  - Commercial and strategic attractiveness

--------------------------------
2. CLINICAL PIPELINE SNAPSHOT
--------------------------------
- Total number of trials
- Phase-wise distribution
- Recruitment status
- Key sponsors
- Key investigational therapies

--------------------------------
3. SCIENTIFIC & MEDICAL INSIGHTS
--------------------------------
- Key biological pathways and mechanisms
- Summary of recent scientific findings
- Strength and maturity of evidence

--------------------------------
4. PATENT & IP POSITION
--------------------------------
- Active vs expired patents
- Key assignees
- FTO risk level (Low / Medium / High)
- White-space opportunity assessment

--------------------------------
5. MARKET & PRICING OUTLOOK
--------------------------------
- Estimated market size range
- Growth outlook (CAGR trend)
- Competitive intensity
- Pricing constraints

--------------------------------
6. REGULATORY & ACCESS CONSIDERATIONS
--------------------------------
- Approval landscape
- Key safety or regulatory risks
- Market access challenges

--------------------------------
7. SUPPLY CHAIN & TRADE INSIGHTS
--------------------------------
- Import/export dependency
- Sourcing risks
- Country-level exposure

--------------------------------
8. STRATEGIC OPPORTUNITIES & RISKS
--------------------------------
- Key repurposing opportunities
- Partnership / licensing potential
- Development bottlenecks
- Regulatory & IP risks

--------------------------------
9. FINAL STRATEGIC RECOMMENDATIONS
--------------------------------
- Go / No-Go outlook
- Suggested R&D focus areas
- Suggested commercial strategy
- Risk mitigation priorities

--------------------------------
10. DATA RELIABILITY & LIMITATIONS
--------------------------------
- Real vs simulated data split
- Data gaps

--------------------------------
--------------------------------
IMPORTANT CONSTRAINTS (STRICT)
--------------------------------
- **NO HALLUCINATION:** If a section has "Data not available", explicitly state "Data not available from live sources" for that section. DO NOT invent numbers.
- **NO GENERIC TEXT:** Do not write generic educational content (e.g., "mRNA vaccines work by..."). Only report on SPECIFIC findings from the input data.
- **NO PLACEHOLDERS:** Do not use "Leader A", "Leader B", or "$2.5B" unless it appears in the REAL input data.
- **PROFESSIONAL FORMAT:** Use clean Markdown. No bullet points except in lists.
- **LENGTH:** Concise. 1.5 pages max.
"""

        # 3. Call LLM
        messages = [
            {"role": "system", "content": "You are a senior pharmaceutical strategy consultant."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.llm_manager.generate(
            messages=messages,
            provider="openai", # Force OpenAI for high quality report
            model="gpt-4o",    # Use high quality model
            temperature=0.3,   # Low temperature for factual consistency
            max_tokens=3000
        )
        
        return response["content"]
