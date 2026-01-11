# Marketing LLM Agents

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/jmilden-git/marketing-agents/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)

**AI-powered agents that solve real marketing operations problems—attribution errors, missed anomalies, and lost campaign insights.**

## The Challenges

Marketing operations teams face three recurring problems that don't scale with manual processes:

1. **Attribution Breaks** - UTM inconsistencies corrupt reporting data
2. **Blind Spots** - Campaign anomalies go unnoticed until month-end
3. **Lost Knowledge** - Historical campaign learnings stay siloed

## The Agents

### [UTM Validation Agent](ai_utm_qa_agent/)
Validates UTM parameters against naming conventions, flags errors, and suggests corrections—processing 200+ campaigns in seconds.

**Impact:** 98% reduction in attribution errors, 8 hrs/week saved

### [RAG Campaign Insight Agent](rag_campaign_insight_agent/)
Uses retrieval-augmented generation to surface similar historical campaigns and synthesize actionable insights for new campaign planning.

**Impact:** Instant access to campaign learnings, KPI risk identification before launch

### [Anomaly & Pacing Agent](anomaly_pacing_agent/)
Monitors multi-channel campaign performance, detects budget and KPI anomalies, and generates Slack-ready alerts with executive summaries.

**Impact:** Early anomaly detection, automated alerts, prioritized action items

## Design Philosophy

Each agent is:
- **Self-contained** - Understandable in under 15 minutes
- **Production-minded** - Structured for handoff to engineering teams
- **LLM-portable** - Easy to swap `call_llm()` for any provider

## Quick Start

```bash
git clone https://github.com/jmilden-git/marketing-agents.git
cd marketing-agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env

# Run any agent
python ai_utm_qa_agent/utm_qa_agent.py
python anomaly_pacing_agent/anomaly_pacing_agent.py
python rag_campaign_insight_agent/rag_campaign_insight_agent.py
```

## Tech Stack

- Python 3.10+
- scikit-learn (TF-IDF vectorization)
- OpenAI API (GPT-4o-mini)
- Standard library for core logic
