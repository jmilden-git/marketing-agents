# Marketing LLM Agents

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/jmilden-git/marketing-agents/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)

A small collection of hands-on MVP agents that demonstrate how I approach the Alteryx AI Operations Lead problem space:

- AI UTM and Tag QA Agent
- RAG Campaign Insight Agent
- AI Anomaly and Pacing Monitoring Agent

Each project is:

- Built as a small, self-contained proof of concept
- Designed to be understandable in under fifteen minutes
- Structured so it can be handed off to Data Science, Platform, or Web Engineering for scaling

## Projects

1. **AI UTM and Tag QA Agent**  
   Validates URLs and UTM parameters against a marketing taxonomy, suggests fixes, and generates a marketer friendly QA summary.

   Folder: [`ai_utm_qa_agent`](ai_utm_qa_agent/)

2. **RAG Campaign Insight Agent**  
   Uses a lightweight retrieval approach to find similar past campaigns and synthesize insights, recommendations, and KPI risk callouts.

   Folder: [`rag_campaign_insight_agent`](rag_campaign_insight_agent/)

3. **AI Anomaly and Pacing Monitoring Agent**  
   Monitors synthetic multi channel campaign performance, detects anomalies, and produces structured alerts plus narrative commentary.

   Folder: [`anomaly_pacing_agent`](anomaly_pacing_agent/)

## Tech stack

- Python 3.10+
- Standard library only for core logic
- `scikit-learn` and `pyyaml` for the RAG demo
- Design assumes easy swapping of the `call_llm` stub with a real LLM provider

## Installation

```bash
git clone https://github.com/jmilden-git/marketing-agents.git
cd marketing-agents
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
