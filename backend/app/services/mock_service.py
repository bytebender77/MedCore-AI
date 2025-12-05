from typing import List, Dict, Any

class MockService:
    @staticmethod
    def get_mock_clinical_trials(query: str) -> List[Dict[str, Any]]:
        """Return mock clinical trial results"""
        phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
        statuses = ["Recruiting", "Active, not recruiting", "Completed"]
        
        # Extract a title-like string from query if possible, else use query
        title_term = query.split()[0] if query else "Treatment"
        
        return [
            {
                "nct_id": f"NCT0{i+400:05d}",
                "title": f"Study of {title_term} in Cancer Treatment - Trial {i+1}",
                "condition": ["Cancer", "Solid Tumor"],
                "phase": phases[i % len(phases)],
                "status": statuses[i % len(statuses)],
                "sponsor": f"Research Institute {chr(65+i)}",
                "url": f"https://clinicaltrials.gov/study/NCT0{i+400:05d}"
            }
            for i in range(5)
        ]

    @staticmethod
    def get_mock_pubmed_results(query: str) -> List[Dict[str, Any]]:
        """Return mock PubMed results"""
        return [
            {
                "pmid": f"3{i:07d}",
                "title": f"Clinical study on {query} - Systematic review and meta-analysis",
                "authors": ["Smith J", "Johnson A", "Williams B"],
                "source": "Journal of Clinical Oncology",
                "pubdate": "2023",
                "doi": f"10.1001/jco.2023.{i:04d}",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/3{i:07d}/"
            }
            for i in range(5)
        ]

    @staticmethod
    def get_mock_patents(query: str) -> List[Dict[str, Any]]:
        """Return mock USPTO patent results"""
        # Extract key terms for realistic titles
        key_terms = query.split()[:3]
        term_str = " ".join(key_terms) if key_terms else "Pharmaceutical"
        
        return [
            {
                "patent_number": f"US{11000000 + i}",
                "title": f"Pharmaceutical composition comprising {term_str} for therapeutic use",
                "assignee": f"Global Pharma Corp {chr(65+i)}",
                "filing_date": "2021-05-15",
                "grant_date": "2023-02-10",
                "status": "Active" if i < 3 else "Pending",
                "url": f"https://patents.google.com/patent/US{11000000 + i}"
            }
            for i in range(5)
        ]

    @staticmethod
    def get_mock_trade_data(query: str) -> Dict[str, Any]:
        """Return mock UN Comtrade data"""
        return {
            "commodity": "Pharmaceutical Products",
            "hs_code": "3004",
            "top_exporters": [
                {"partner": "Germany", "value_usd": 85000000000},
                {"partner": "Switzerland", "value_usd": 78000000000},
                {"partner": "USA", "value_usd": 65000000000},
                {"partner": "Ireland", "value_usd": 55000000000},
                {"partner": "Belgium", "value_usd": 48000000000}
            ],
            "top_importers": [
                {"partner": "USA", "value_usd": 120000000000},
                {"partner": "Germany", "value_usd": 60000000000},
                {"partner": "China", "value_usd": 45000000000}
            ],
            "trend": "Stable growth of 5-7% annually",
            "note": "Simulated trade data for demonstration"
        }
