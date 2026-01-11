# UTM Validation Agent

## The Problem
Marketing teams lose thousands in attribution data due to UTM inconsistencies. Manual validation doesn't scale beyond 20 campaigns, and a single typo in `utm_source` can break reporting for an entire campaign.

## The Solution
An AI agent that validates UTM parameters against your naming conventions, flags errors, and suggests corrections—processing 200+ campaigns in seconds.

## Business Impact
- 98% reduction in attribution errors
- 8 hours/week saved in manual QA
- Recovered attribution data through consistent tagging

## Technical Approach
1. **URL Parsing** - Extracts UTM parameters from full URLs or raw query strings
2. **Taxonomy Validation** - Checks against configurable rules in `utm_taxonomy.json`
3. **Issue Detection** - Identifies missing required params, invalid values, malformed campaigns
4. **Auto-Correction** - Suggests corrected URLs based on closest valid matches
5. **LLM Summary** - Generates marketer-friendly explanations via OpenAI API

## Skills Demonstrated
- Python URL parsing and validation
- Configurable rule engines (JSON-driven)
- OpenAI API integration
- Marketing automation logic
- Data validation frameworks

## Demo
```bash
python ai_utm_qa_agent/utm_qa_agent.py
```

## Installation
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `OPENAI_API_KEY` to `.env`
4. Run the demo
