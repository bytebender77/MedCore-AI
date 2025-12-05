# Pharmaceutical Agentic AI Research Platform

A production-ready multi-agent AI system for pharmaceutical research, supporting both OpenAI (ChatGPT) and Google (Gemini) models.

## Features

- 🤖 Multi-agent orchestration (7 specialized agents)
- 🔍 Real-time web scraping from PubMed, ClinicalTrials.gov, USPTO
- 📊 Automated report generation
- 💰 Cost tracking and rate limiting
- 🎨 Modern React UI
- 🐳 Docker containerization

## Quick Start

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key
- Google AI API Key

### Installation

1. Clone repository:
```bash
git clone <repository-url>
cd pharma-agent-ai




lsof -ti:8000 | xargs kill -9

cd backend
./.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


cd frontend
PORT=3001 npm start