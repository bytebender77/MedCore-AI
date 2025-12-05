from typing import Dict, Any

class DataSource:
    def __init__(self, name: str, url: str, category: str, description: str, auth_required: bool = False):
        self.name = name
        self.url = url
        self.category = category
        self.description = description
        self.auth_required = auth_required

DATA_SOURCES: Dict[str, DataSource] = {
    # Clinical Trials
    "clinical_trials_gov": DataSource(
        "ClinicalTrials.gov API", 
        "https://clinicaltrials.gov/api/v2/studies", 
        "Clinical Trials", 
        "US National Library of Medicine protocol registration system"
    ),
    "who_ictrp": DataSource(
        "WHO ICTRP", 
        "https://trialsearch.who.int/", 
        "Clinical Trials", 
        "World Health Organization International Clinical Trials Registry Platform"
    ),
    "eu_ctr": DataSource(
        "EU Clinical Trials Register", 
        "https://www.clinicaltrialsregister.eu/", 
        "Clinical Trials", 
        "European Union Clinical Trials Register"
    ),
    
    # Scientific Literature
    "pubmed": DataSource(
        "PubMed (NCBI) API", 
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/", 
        "Scientific Literature", 
        "Biomedical literature from MEDLINE, life science journals, and online books"
    ),
    "pmc": DataSource(
        "PubMed Central (PMC)", 
        "https://www.ncbi.nlm.nih.gov/pmc/", 
        "Scientific Literature", 
        "Free full-text archive of biomedical and life sciences journal literature"
    ),
    "openalex": DataSource(
        "OpenAlex", 
        "https://api.openalex.org/", 
        "Scientific Literature", 
        "Open and comprehensive catalog of scholarly papers, authors, institutions, and more"
    ),
    "semantic_scholar": DataSource(
        "Semantic Scholar", 
        "https://api.semanticscholar.org/", 
        "Scientific Literature", 
        "AI-driven research tool for scientific literature"
    ),
    "core_ac_uk": DataSource(
        "CORE", 
        "https://core.ac.uk/services/api", 
        "Scientific Literature", 
        "Aggregating the world's open access research papers"
    ),

    # Patents
    "uspto": DataSource(
        "USPTO Patent API", 
        "https://developer.uspto.gov/ibd-api", 
        "Patents", 
        "United States Patent and Trademark Office"
    ),
    "epo_ops": DataSource(
        "EPO Open Patent Services", 
        "https://ops.epo.org/", 
        "Patents", 
        "European Patent Office",
        auth_required=True
    ),
    "google_patents": DataSource(
        "Google Patents", 
        "https://patents.google.com/", 
        "Patents", 
        "Search engine that indexes patents and patent applications"
    ),
    "lens_org": DataSource(
        "Lens.org", 
        "https://api.lens.org/", 
        "Patents", 
        "Patent and scholarly search",
        auth_required=True
    ),
    "wipo_patentscope": DataSource(
        "WIPO Patentscope", 
        "https://patentscope.wipo.int/", 
        "Patents", 
        "World Intellectual Property Organization"
    ),

    # Disease Burden
    "who_gho": DataSource(
        "WHO Global Health Observatory", 
        "https://ghoapi.azureedge.net/api/", 
        "Disease Burden", 
        "WHO's gateway to health-related statistics"
    ),
    "ihme_gbd": DataSource(
        "IHME Global Burden of Disease", 
        "https://vizhub.healthdata.org/gbd/", 
        "Disease Burden", 
        "Institute for Health Metrics and Evaluation"
    ),
    "globocan": DataSource(
        "GLOBOCAN", 
        "https://gco.iarc.fr/", 
        "Disease Burden", 
        "Global Cancer Observatory"
    ),

    # Drug Regulatory
    "fda_drugs": DataSource(
        "US FDA Drug Data", 
        "https://api.fda.gov/drug/drugsfda.json", 
        "Drug Regulatory", 
        "FDA approved drugs"
    ),
    "fda_labels": DataSource(
        "FDA Drug Labels", 
        "https://api.fda.gov/drug/label.json", 
        "Drug Regulatory", 
        "FDA drug labeling"
    ),
    "ema": DataSource(
        "European Medicines Agency", 
        "https://www.ema.europa.eu/", 
        "Drug Regulatory", 
        "EMA medicines data"
    ),
    "cdsco": DataSource(
        "CDSCO India", 
        "https://cdsco.gov.in/", 
        "Drug Regulatory", 
        "Central Drugs Standard Control Organisation"
    ),
    "who_prequal": DataSource(
        "WHO Prequalification", 
        "https://extranet.who.int/prequal/", 
        "Drug Regulatory", 
        "WHO Prequalification of Medical Products"
    ),

    # Trade
    "un_comtrade": DataSource(
        "UN Comtrade", 
        "https://comtradeapi.worldbank.org/v1/get/HS", 
        "Trade", 
        "United Nations Commodity Trade Statistics Database",
        auth_required=True
    ),
    "wits": DataSource(
        "World Bank WITS", 
        "https://wits.worldbank.org/", 
        "Trade", 
        "World Integrated Trade Solution"
    ),
    "dgft": DataSource(
        "DGFT India", 
        "https://www.dgft.gov.in/", 
        "Trade", 
        "Directorate General of Foreign Trade"
    ),

    # Pricing
    "nppa": DataSource(
        "NPPA India", 
        "https://www.nppaindia.nic.in/", 
        "Pricing", 
        "National Pharmaceutical Pricing Authority"
    ),
    "cms_medicare": DataSource(
        "CMS Medicare", 
        "https://data.cms.gov/", 
        "Pricing", 
        "Centers for Medicare & Medicaid Services"
    ),
    "gov_in_pricing": DataSource(
        "Open Government Data India", 
        "https://data.gov.in/", 
        "Pricing", 
        "Open Government Data (OGD) Platform India"
    ),

    # News
    "google_news": DataSource(
        "Google News RSS", 
        "https://news.google.com/rss/search?q=pharma", 
        "News", 
        "Google News Search for Pharma"
    ),
    "gdelt": DataSource(
        "GDELT", 
        "https://api.gdeltproject.org/api/v2/doc/doc", 
        "News", 
        "Global Database of Events, Language, and Tone"
    ),
    "fiercepharma": DataSource(
        "FiercePharma", 
        "https://www.fiercepharma.com/", 
        "News", 
        "Pharma industry news"
    ),
    "biopharmadive": DataSource(
        "BioPharmaDive", 
        "https://www.biopharmadive.com/", 
        "News", 
        "BioPharma industry news"
    ),
}
