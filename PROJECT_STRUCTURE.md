# Project Structure

## Overview
This document outlines the file structure of the Pharma AI Research Platform.

## Directory Tree

```
.
├── Makefile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── app
│   │   ├── __init__.py
│   │   ├── agents
│   │   │   ├── base_agent.py
│   │   │   ├── clinical_trials_agent.py
│   │   │   ├── master_agent.py
│   │   │   ├── patent_landscape_agent.py (Missing/Merged into worker_agents.py)
│   │   │   ├── web_intelligence_agent.py
│   │   │   └── worker_agents.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── main.py
│   │   ├── models
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── clinical_trials_service.py
│   │   │   ├── mock_service.py
│   │   │   ├── patent_service.py
│   │   │   ├── pubmed_service.py
│   │   │   └── trade_service.py
│   │   └── utils
│   │       └── helpers.py
│   ├── requirements.txt
│   └── tests
├── backendrun.text
├── docker-compose.yml
├── docs
│   └── USER_GUIDE.md
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── LandingPage.css
│       ├── LandingPage.js
│       ├── components
│       │   ├── AgentResultDisplay.js
│       │   └── ...
│       ├── index.css
│       ├── index.js
│       ├── logo.svg
│       ├── reportWebVitals.js
│       ├── setupTests.js
│       └── styles
│           └── theme.js
└── reports
    └── (Generated PDF Reports)
```

## Key Directories

### `/backend`
Contains the FastAPI application source code.
- `app/agents`: Logic for the AI agents (Clinical Trials, Patents, Web Intelligence).
- `app/services`: External API integrations (PubMed, PatentsView, ClinicalTrials.gov).
- `app/core`: Configuration and database settings.

### `/frontend`
Contains the React application source code.
- `src/components`: Reusable UI components.
- `src/LandingPage.js`: The main entry page for the application.
- `src/App.js`: The core application logic and dashboard.

### `/docs`
Documentation files including the User Guide.
