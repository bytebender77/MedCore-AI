# Pharmaceutical Agentic AI Research Platform

A production-ready multi-agent AI system for pharmaceutical research, supporting both OpenAI (ChatGPT) and Google (Gemini) models.

## Features

- 🤖 Multi-agent orchestration (7 specialized agents)
- 🔍 Real-time web scraping from PubMed, ClinicalTrials.gov, The Lens, UN Comtrade
- 📊 Automated PDF report generation with citations
- 💰 Cost tracking and rate limiting
- 🎨 Modern React UI with glassmorphism design
- 🐳 Docker containerization
- 🧠 Dual-LLM support (OpenAI GPT-4 + Google Gemini)

---

## 📝 Sample Queries

### 🔬 Drug Repurposing & Research

| # | Query | What It Does |
|---|-------|--------------|
| 1 | `Analyze Metformin repurposing opportunities for cardiovascular diseases` | Explores non-diabetic uses of Metformin based on clinical trials and literature |
| 2 | `What are the emerging therapeutic applications of GLP-1 agonists beyond diabetes?` | Investigates weight loss, NASH, and neurological applications of GLP-1 drugs |
| 3 | `Identify drug repurposing candidates for Alzheimer's disease from existing cancer therapies` | Cross-references oncology drugs with neurodegeneration research |

### 📜 Patent Landscape Analysis

| # | Query | What It Does |
|---|-------|--------------|
| 4 | `Analyze patent landscape for CAR-T cell therapy in solid tumors` | Maps patent filings, key assignees, and expiration timelines for CAR-T |
| 5 | `Which companies hold the most patents for mRNA vaccine delivery systems?` | Identifies IP leaders in mRNA technology (Moderna, BioNTech, etc.) |
| 6 | `Patent expiry analysis for top 10 biologics in the US market` | Tracks biosimilar opportunities from upcoming patent cliffs |

### 🏥 Clinical Trials Intelligence

| # | Query | What It Does |
|---|-------|--------------|
| 7 | `Find active Phase 3 clinical trials for non-small cell lung cancer immunotherapy` | Returns recruiting trials with enrollment data and endpoints |
| 8 | `What are the latest clinical trials for CRISPR-based gene therapies?` | Discovers cutting-edge gene editing trials globally |
| 9 | `Compare clinical trial activity for obesity drugs: Ozempic vs Mounjaro vs Zepbound` | Head-to-head trial comparison with phase distribution |
| 10 | `Identify orphan drug clinical trials for rare pediatric diseases in India` | Filters trials by geography and regulatory designation |

### 💰 Market & Pricing Intelligence

| # | Query | What It Does |
|---|-------|--------------|
| 11 | `Analyze US Medicare pricing trends for diabetes medications 2020-2024` | Extracts CMS pricing data with year-over-year analysis |
| 12 | `Compare drug pricing: Generic vs Branded statins in India` | NPPA price analysis for cardiovascular drugs |
| 13 | `What is the market size and growth forecast for biosimilars in oncology?` | Market intelligence with competitive landscape |

### 🚢 Trade & Supply Chain Analysis

| # | Query | What It Does |
|---|-------|--------------|
| 14 | `Analyze global import/export trends for pharmaceutical APIs from India to US` | UN Comtrade data on API trade flows |
| 15 | `Which countries are the largest exporters of vaccine raw materials?` | Global trade intelligence for biologics supply chain |

### 🧬 Complex Multi-Domain Queries

| # | Query | What It Does |
|---|-------|--------------|
| 16 | `Comprehensive analysis of Pembrolizumab: patents, trials, pricing, and trade data` | Full 360° intelligence report across all agents |
| 17 | `Identify white space opportunities in the NASH therapeutic landscape` | Gap analysis combining trials, patents, and market data |
| 18 | `Research antibiotic resistance: clinical pipeline, patent activity, and global trade patterns` | Multi-source intelligence on AMR |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API Key
- Google AI API Key (optional)

### Installation

1. **Clone repository:**
```bash
git clone <repository-url>
cd pharma-agent-ai
```

2. **Backend Setup:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup:**
```bash
cd frontend
npm install
```

4. **Environment Variables:**
```bash
# Backend (.env)
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LENS_API_KEY=your_lens_key
COMTRADE_API_KEY=your_comtrade_key
```

### Running Locally

```bash
# Terminal 1 - Backend
cd backend
./.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
PORT=3001 npm start
```

### Utility Commands

```bash
# Kill existing backend process
lsof -ti:8000 | xargs kill -9

# Kill existing frontend process
lsof -ti:3001 | xargs kill -9
```

---

## 📊 System Architecture

```
User Query → Master Agent → [6 Parallel Workers] → LLM Synthesis → PDF Report
                              ├── Clinical Trials Agent (ClinicalTrials.gov)
                              ├── Patent Agent (The Lens)
                              ├── Web Intelligence Agent (PubMed)
                              ├── Market Agent (CMS/NPPA)
                              ├── EXIM Agent (UN Comtrade)
                              └── Internal Knowledge Agent (Local Docs)
```

---

## 📄 License

MIT License - See LICENSE file for details