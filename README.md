# 🧠 Synapse

**Multi-Agent Business Intelligence & Decision Support**

Synapse is one business assistant powered by a team of seven specialized AI agents.
A user asks a plain-language question — *"Our sales dropped 20%, why, and what should we do?"* —
a Manager agent decides which specialists to involve, each analyzes its part
(data, finance, market, customers, risk), and a Strategy agent combines everything
into one evidence-based recommendation. It runs on **Microsoft Foundry** using the
**gpt-4.1-mini** model.

> Decision *support*, not automation — Synapse recommends; the human decides.

---

## How it works

```
USER (uploads data + asks a question)
        │
        ▼
🧠 Manager Agent  — decides which specialists are needed
        │
 ┌──────┬──────┬──────┬──────┐
 ▼      ▼      ▼      ▼
📊      💰      🔍      👥
Analytics Finance Market Customer   (run in parallel)
 └──────┴──────┴──────┴──────┘
        ▼
      ⚠️ Risk        — weighs every finding
        ▼
      🎯 Strategy    — one prioritized recommendation
        ▼
     📋 Final Business Report → USER
```

The Manager only calls the agents a question actually needs — a simple lookup uses
one agent; a complex decision triggers the full chain.

## The seven agents

| Agent | Role | What it does |
|-------|------|--------------|
| 🧠 Manager | Orchestrator | Routes the question, gathers findings, returns the final report |
| 📊 Analytics | Data Analyst | Revenue, growth, margins, KPIs, per-product trends |
| 💰 Finance | CFO | Margins, ROI, break-even, cash flow, scenarios |
| 🔍 Market | Market Research | Competitors, pricing, market trends |
| 👥 Customer | Customer Intelligence | Review sentiment, complaints, churn risk |
| ⚠️ Risk | Risk Manager | Financial / market / operational / customer risk + mitigations |
| 🎯 Strategy | Decision Support | Synthesizes everything into one recommendation |

## Tech stack

- **Platform:** Microsoft Foundry (agents, tools, orchestration)
- **Model:** gpt-4.1-mini (one shared deployment)
- **Backend:** FastAPI (`/upload`, `/analyze`, serves the frontend)
- **Data analysis:** Code Interpreter · **Documents:** RAG / Azure AI Search · **External:** Web search
- **Frontend:** plain HTML/CSS/JS (landing page + console)

## Project structure

```
Synapse/
├── backend/
│   ├── server.py            # FastAPI: serves pages + /upload, /analyze
│   ├── orchestrator.py      # runs the 7-agent pipeline
│   ├── foundary_client.py   # Azure Foundry connection
│   ├── search_client.py     # Azure AI Search
│   ├── rag.py               # retrieval
│   ├── document_processor.py
│   ├── business_context.py
│   ├── config.py
│   ├── requirements.txt
│   └── agents/              # analytics, finance, market, customer, risk, strategy
├── frontend/
│   ├── index.html           # landing page
│   └── console.html         # the app — upload data, ask, get the report
└── README.md
```

## Prerequisites

- Python 3.10+
- Azure CLI — `brew install azure-cli`
- Access to the team's Azure Foundry project + AI Search resource

## Setup

```
cd backend
pip install -r requirements.txt
az login                 # sign in with an account that has Foundry access
```

Create `backend/.env` with the Azure credentials and endpoints (ask the backend owner).
**Never commit `.env`** — it holds secrets.

## Run

```
cd backend
uvicorn server:app --reload --port 8000
```

Then open:
- **http://localhost:8000/** — landing page
- **http://localhost:8000/console.html** — the console: upload data, ask a question, get the report

## Usage

1. Upload business files (PDF, DOCX, Excel, CSV, TXT).
2. Ask a plain-language question.
3. Watch the agents run, click any agent to see its findings, and read the final Business Report.
