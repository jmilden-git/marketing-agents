# AI UTM and Tag QA Agent

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

This agent validates URLs and UTM parameter blocks against a simple marketing taxonomy. It identifies missing or invalid parameters, suggests corrected URLs, and generates an LLM summary suitable for marketers.

## Files

- `utm_qa_agent.py`  
  Core agent logic, CLI demo, and LLM call stub.

- `utm_taxonomy.json`  
  Required parameters, allowed values, and default channel mappings.

- `examples/sample_inputs.md`  
  Sample URLs and parameter blocks used in testing.

## Running the demo

From the repo root:

```bash
python ai_utm_qa_agent/utm_qa_agent.py
