# Architecture Overview

This repo contains three independent but related AI agent POCs that mirror key responsibilities of an AI Operations Lead role.

- **UTM QA Agent**  
  Focuses on data quality and governance at the point of campaign creation.

- **RAG Campaign Insight Agent**  
  Focuses on insight retrieval and decision support for GTM planning.

- **Anomaly and Pacing Agent**  
  Focuses on monitoring, guardrails, and near real time commentary.

Each agent has:

- A deterministic core for reliability and debuggability.
- A small knowledge layer (taxonomy, KPI dictionary, or metrics).
- A thin LLM interface that can be swapped for any provider.
- A CLI entry point to keep the POCs easy to demo.
