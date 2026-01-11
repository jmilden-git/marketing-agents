
# README
**File:** `anomaly_pacing_agent/README.md`

```markdown
# AI Anomaly and Pacing Monitoring Agent

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

This agent simulates multi channel campaign metrics, detects anomalies, and generates both structured alerts and narrative explanations.  
It demonstrates how deterministic rules and LLM commentary can work together to support GTM monitoring.

---

## Features

- Synthetic multi channel metric generation  
- Overspend and underspend detection  
- CPA guardrail checks  
- CTR and CVR underperformance detection  
- JSON anomaly output  
- Slack style alert formatting  
- LLM style narrative summaries for GTM meetings  

---

## File Structure
anomaly_pacing_agent/
├─ README.md
└─ anomaly_pacing_agent.py


---

## Running the Demo

From the repository root:

```bash
python anomaly_pacing_agent/anomaly_pacing_agent.py

You will see:
JSON anomalies
Slack friendly summary
LLM executive summary and action plan

