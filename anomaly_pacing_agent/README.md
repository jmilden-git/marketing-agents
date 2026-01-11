# Anomaly & Pacing Monitoring Agent

## The Problem
Campaign overspend and underperformance often go unnoticed until end-of-month reporting. By then, budgets are blown and optimization windows are missed. Manual monitoring across multiple channels doesn't scale.

## The Solution
An AI agent that monitors multi-channel campaign performance in real-time, detects anomalies against configurable guardrails, and produces both structured alerts and executive summaries.

## Business Impact
- Early detection of budget anomalies (overspend/underspend)
- Immediate visibility into CPA, CTR, and CVR violations
- Automated Slack-ready alerts for faster response
- Executive summaries with prioritized action items

## Technical Approach
1. **Guardrail Configuration** - Define thresholds in `pacing_plan.json` (daily budget, max CPA, min CTR/CVR)
2. **Anomaly Detection** - Rule-based engine detects 5 anomaly types:
   - Overspend (>25% above daily budget)
   - Underspend (<25% below daily budget)
   - CPA violations (above guardrail)
   - CTR underperformance (70% of rolling average)
   - CVR shortfalls (below minimum)
3. **Alert Formatting** - Structured JSON output + Slack-ready messages
4. **LLM Narratives** - Executive summaries with context and recommended actions

## Skills Demonstrated
- Real-time monitoring logic
- Guardrail-based anomaly detection
- Multi-channel campaign analytics
- OpenAI API integration
- Slack-style alert formatting

## Demo
```bash
python3 anomaly_pacing_agent/anomaly_pacing_agent.py
```

## Installation
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `OPENAI_API_KEY` to `.env`
4. Configure guardrails in `pacing_plan.json`
5. Run the demo
