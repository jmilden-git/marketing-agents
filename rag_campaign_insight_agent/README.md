
---

### 4.2 `rag_campaign_insight_agent/README.md`

```markdown
# RAG Campaign Insight Agent

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

This agent retrieves similar historical campaigns and synthesizes insights, recommendations, and KPI risks for a new campaign brief. It is a lightweight demonstration of RAG style reasoning in a GTM context.

## Files

- `rag_campaign_insight_agent.py`  
  Campaign corpus builder, similarity search, and LLM insight generator.

- `campaign_history.json`  
  Synthetic campaign records with channels, objectives, and KPIs.

- `kpi_dictionary.yaml`  
  Definitions for key performance indicators used in analysis.

## Running the demo

From the repo root:

```bash
python3 rag_campaign_insight_agent/rag_campaign_insight_agent.py
