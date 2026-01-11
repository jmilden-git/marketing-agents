# Contributing to the Project

Thank you for contributing! To maintain code quality and a smooth workflow, please follow these guidelines.

## Environment Setup
1. **Clone the repository:** `git clone <repo-url>`
2. **Create virtual environment:** `python -m venv .venv && source .venv/bin/activate`
3. **Install dependencies:** `pip install -r requirements.txt`
4. **Environment Variables:** Copy `.env.example` to `.env` and add your `OPENAI_API_KEY`.

## Branching Strategy
* **ALWAYS** create a feature branch before starting major changes.
* **NEVER** commit directly to `main`.
* **Branch Naming Convention:**
    * `feature/short-description`
    * `fix/short-description`
    * `docs/short-description`

## Git Workflow
1. **Create branch:** `git checkout -b feature/your-feature-name`
2. **Develop:** Make your changes and commit locally.
3. **Test Locally:**
    * `python -m pytest` – Run all tests
    * `python <agent_dir>/<agent>.py` – Run agent demo
4. **Push:** `git push -u origin feature/your-feature-name`
5. **Pull Request:** Create a PR to merge into `main`.

## Commit Standards
* **Focus:** Keep commits focused on a single change or logical unit.
* **Messages:** Write clear, descriptive commit messages (e.g., `feat: add UTM validation for new channels`).
* **Format:** We recommend [Conventional Commits](https://www.conventionalcommits.org/).

## Code Standards
* **Typing:** Use type hints for all function signatures.
* **Style:** Follow PEP 8 guidelines.
* **Functions:** Keep functions small, focused, and testable.
* **No unnecessary abstractions:** Standard library first for core logic.

## Pull Requests (PRs)
* PRs are required for **all** changes to `main`.
* **NEVER** force push to `main`.
* **Descriptions:** Include a clear summary of *what* changed and *why*.

## Pre-Push Checklist
Before pushing your code, verify the following:
1. [ ] `python -m pytest` passes.
2. [ ] Agent demos run without errors.
3. [ ] All new functions have type hints.

---

# Project Context for Claude Code

## Project Overview

**Marketing LLM Agents** is a collection of three independent proof-of-concept AI agents demonstrating practical AI/ML capabilities for Go-To-Market (GTM) operations. Each agent showcases a different approach to solving marketing operations challenges using LLMs.

### The Three Agents

1. **AI UTM and Tag QA Agent** - Validates marketing URLs and UTM parameters against a taxonomy
2. **RAG Campaign Insight Agent** - Uses retrieval-augmented generation for campaign insights
3. **AI Anomaly and Pacing Monitoring Agent** - Monitors campaign performance and detects anomalies

## Architecture

### Tech Stack
- **Language:** Python 3.10+
- **ML/Data:** scikit-learn (TF-IDF vectorization, cosine similarity)
- **LLM Integration:** OpenAI API (GPT-4o-mini)
- **Configuration:** YAML, JSON
- **Testing:** pytest

### Project Structure
```
marketing-agents/
├── shared/                           # Common utilities
│   ├── __init__.py
│   └── llm.py                        # Unified LLM call interface
├── ai_utm_qa_agent/                  # UTM validation agent
│   ├── __init__.py
│   ├── utm_qa_agent.py               # Core logic
│   ├── utm_taxonomy.json             # Validation rules
│   ├── examples/
│   │   └── sample_inputs.md          # Test cases
│   └── README.md
├── anomaly_pacing_agent/             # Anomaly detection agent
│   ├── __init__.py
│   ├── anomaly_pacing_agent.py       # Core logic
│   ├── pacing_plan.json              # Performance guardrails
│   └── README.md
├── rag_campaign_insight_agent/       # RAG insight agent
│   ├── __init__.py
│   ├── rag_campaign_insight_agent.py # Core logic
│   ├── campaign_history.json         # Sample campaign data
│   ├── kpi_dictionary.yaml           # KPI definitions
│   └── README.md
├── tests/                            # Test suite
│   ├── conftest.py
│   ├── test_utm_qa_agent.py
│   ├── test_anomaly_pacing_agent.py
│   └── test_rag_campaign_insight_agent.py
├── docs/                             # Architecture documentation
│   ├── ARCHITECTURE_OVERVIEW.md
│   ├── UTM_QA_AGENT_DIAGRAM.md
│   ├── ANOMALY_PACING_AGENT_DIAGRAM.md
│   └── RAG_INSIGHT_AGENT_DIAGRAM.md
├── screenshots/                      # Demo screenshots
├── .github/workflows/ci.yml          # CI pipeline
├── pyproject.toml                    # Project configuration
├── requirements.txt                  # Dependencies
└── README.md                         # Project overview
```

## Key Design Principles

1. **Self-Contained POCs:** Each agent is independent and understandable in under 15 minutes
2. **Deterministic Core + Thin LLM Layer:** Business logic is rule-based; LLM calls are isolated
3. **Easy Provider Swapping:** `call_llm()` in `shared/llm.py` can be swapped for any LLM provider
4. **Standard Library First:** Core logic uses only standard library where possible
5. **CLI Entry Points:** Each agent has a `demo()` function for easy testing
6. **Handoff Ready:** Code structured for easy transition to platform/data science teams

## Agent Details

### AI UTM and Tag QA Agent
**Location:** `ai_utm_qa_agent/`

**Purpose:** Validates marketing URLs and UTM parameters against a taxonomy, identifies issues, suggests fixes, and generates marketer-friendly summaries.

**Key Components:**
- `UTMQAAgent` - Main agent class with validation logic
- `UTMCheckResult` - Result dataclass with issues and suggestions
- `utm_taxonomy.json` - Configurable validation rules

**Features:**
- Accepts full URLs or raw query parameters
- Validates required params (utm_source, utm_medium, utm_campaign)
- Checks allowed values against taxonomy
- Validates campaign naming conventions
- Suggests corrected URLs
- Generates LLM summaries for marketers

### RAG Campaign Insight Agent
**Location:** `rag_campaign_insight_agent/`

**Purpose:** Uses retrieval-augmented generation to find similar historical campaigns and synthesize insights for new campaign planning.

**Key Components:**
- `RAGCampaignInsightAgent` - Main agent class
- `CampaignCorpus` - TF-IDF vectorized campaign corpus
- `Campaign` - Campaign data model
- `campaign_history.json` - Historical campaign data
- `kpi_dictionary.yaml` - KPI definitions

**Features:**
- TF-IDF vectorization for similarity search
- Cosine similarity ranking
- Returns top 3 most similar campaigns
- Generates strategic recommendations and KPI risk callouts

### AI Anomaly and Pacing Monitoring Agent
**Location:** `anomaly_pacing_agent/`

**Purpose:** Monitors multi-channel campaign performance, detects anomalies, and produces structured alerts plus narrative commentary.

**Key Components:**
- `AnomalyDetector` - Guardrail-based anomaly detection
- `AnomalyReportingAgent` - Alert formatting and LLM narratives
- `DailyMetrics` - Metrics data model with computed properties
- `Anomaly` - Anomaly data model
- `pacing_plan.json` - Performance guardrails

**Anomaly Types Detected:**
1. Overspend (>25% above daily budget)
2. Underspend (<25% below daily budget)
3. CPA violations (above guardrail)
4. CTR underperformance (70% of rolling average)
5. CVR shortfalls (below minimum)

**Features:**
- Structured JSON anomaly output
- Slack-ready alert formatting
- LLM executive summaries with action items

## Shared Utilities

### LLM Integration (`shared/llm.py`)
```python
from shared import call_llm

response = call_llm(
    prompt="Your prompt here",
    model="gpt-4o-mini",      # Optional, defaults to gpt-4o-mini
    temperature=0.3,          # Optional, defaults to 0.3
    max_tokens=400,           # Optional, defaults to 400
)
```

**LLM Settings:**
- Model: GPT-4o-mini (configurable)
- Temperature: 0.3 (deterministic outputs)
- Max tokens: 400

## Configuration Files

### utm_taxonomy.json (UTM Agent)
```json
{
  "required_params": ["utm_source", "utm_medium", "utm_campaign"],
  "allowed_values": {
    "utm_source": ["email", "google", "linkedin", ...],
    "utm_medium": ["email", "cpc", "social", ...],
    "utm_campaign_prefixes": ["fy25_", "fy26_"]
  },
  "channel_defaults": { ... }
}
```

### pacing_plan.json (Anomaly Agent)
```json
{
  "daily_budget": 1000,
  "max_cpa": 100,
  "min_ctr": 0.02,
  "min_cvr": 0.03
}
```

### kpi_dictionary.yaml (RAG Agent)
```yaml
open_rate: Email engagement metric
click_rate: Email click metric
ctr: Ad click-through rate
conversion_rate: Primary performance KPI
cpl: Cost per lead metric
```

## Common Development Tasks

### Running an Agent Demo
```bash
# UTM QA Agent
python ai_utm_qa_agent/utm_qa_agent.py

# Anomaly Pacing Agent
python anomaly_pacing_agent/anomaly_pacing_agent.py

# RAG Campaign Insight Agent
python rag_campaign_insight_agent/rag_campaign_insight_agent.py
python rag_campaign_insight_agent/rag_campaign_insight_agent.py "Your campaign brief here"
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_utm_qa_agent.py

# Run specific test
python -m pytest tests/test_utm_qa_agent.py::TestUTMQAAgent::test_parse_full_url
```

### Adding a New Agent
1. Create new directory: `new_agent_name/`
2. Add `__init__.py` with public exports
3. Create main agent file with dataclasses and agent class
4. Add configuration files (JSON/YAML)
5. Add `README.md` with usage examples
6. Import `call_llm` from `shared` module
7. Add tests in `tests/test_new_agent.py`
8. Update `docs/` with architecture diagram

### Modifying LLM Integration
1. Edit `shared/llm.py`
2. All agents automatically use the updated implementation
3. To swap providers, modify the `call_llm()` function

### Adding New Validation Rules (UTM Agent)
1. Edit `ai_utm_qa_agent/utm_taxonomy.json`
2. Add new allowed values, required params, or channel defaults
3. No code changes required for config-driven rules

## Important Files to Reference

### Core Business Logic
- `shared/llm.py` - Unified LLM integration
- `ai_utm_qa_agent/utm_qa_agent.py` - URL/UTM validation
- `anomaly_pacing_agent/anomaly_pacing_agent.py` - Anomaly detection
- `rag_campaign_insight_agent/rag_campaign_insight_agent.py` - Campaign similarity search

### Configuration
- `utm_taxonomy.json` - UTM validation rules
- `pacing_plan.json` - Performance guardrails
- `kpi_dictionary.yaml` - KPI definitions
- `campaign_history.json` - Sample campaign data

### Tests
- `tests/test_utm_qa_agent.py` - UTM agent tests
- `tests/test_anomaly_pacing_agent.py` - Anomaly agent tests
- `tests/test_rag_campaign_insight_agent.py` - RAG agent tests

## Important Conventions

### Never Do This
- Commit directly to `main`
- Hard-code API keys or secrets
- Force push to shared branches
- Add unnecessary abstractions
- Skip type hints on function signatures

### Always Do This
- Create feature branches
- Write type hints for all functions
- Add tests for new functionality
- Use environment variables for configuration
- Keep agents self-contained and focused
- Update documentation when adding features

### Code Style
- Use `dataclass` for data models
- Keep functions small and focused (single responsibility)
- Separate business logic from LLM calls
- Use descriptive variable names
- Include docstrings for public APIs

## Environment Variables

Required in `.env`:
```env
OPENAI_API_KEY="sk-..."
```

## Quick Start Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Run demos
python ai_utm_qa_agent/utm_qa_agent.py
python anomaly_pacing_agent/anomaly_pacing_agent.py
python rag_campaign_insight_agent/rag_campaign_insight_agent.py

# Run tests
python -m pytest

# Git workflow
git checkout -b feature/my-feature
git add .
git commit -m "feat: description"
git push -u origin feature/my-feature
```

## Troubleshooting

### OpenAI API errors
- Verify `OPENAI_API_KEY` in `.env`
- Check API key has sufficient credits
- Ensure `python-dotenv` is installed

### Import errors
- Ensure you're running from project root
- Verify `.venv` is activated
- Run `pip install -r requirements.txt`

### Test failures
- Mock LLM calls in tests to avoid API costs
- Check test fixtures match expected data structures
- Ensure all `__init__.py` files are present

## Getting Help

- Review existing agent READMEs in each directory
- Check `docs/` for architecture diagrams
- Reference test files for usage examples
- Check `examples/sample_inputs.md` for UTM test cases
