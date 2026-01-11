# Contributing Guidelines

Thank you for your interest in contributing to the **Alteryx AI Ops LLM Agent POCs** project.  
This repository demonstrates small, production-minded AI agent MVPs aligned with GTM and AI Operations workflows.  
The guidelines below help ensure code quality, reproducibility, and a consistent development experience.

---

## 1. Getting Started

1. Fork the repository.
2. Create a feature branch.
   ```
   git checkout -b feature/my-enhancement
   ```
3. Install the development environment.
   ```
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 2. Code Standards

### Python version  
Use Python 3.10 or higher.

### Style  
- Follow PEP 8 guidelines.  
- Keep functions small, testable, and purposeful.  
- Avoid unnecessary abstractions for these MVPs.

### LLM calls  
- Never commit API keys.  
- Keep `call_llm` methods isolated so they can be swapped for any provider.  
- Keep prompts versioned or commented when relevant.

---

## 3. Project Structure

Each agent follows a predictable pattern:

- Core script implementing deterministic logic  
- Config or metadata files (taxonomy, KPIs, etc.)  
- Example inputs  
- A README describing usage and expected behavior  

When adding a new agent, match this layout for consistency.

---

## 4. Adding New Features

When submitting enhancements:

1. Update or add README sections describing how to use the new feature.  
2. Include example prompts or inputs if applicable.  
3. Ensure your code runs without additional dependencies unless documented.  
4. When appropriate, add comments describing why design choices were made.

---

## 5. Pull Requests

A good pull request:

- Has a clear description of the change  
- Includes references to related issues (if any)  
- Passes basic Python compilation checks  
- Includes updated documentation or examples  

To validate code compiles:

```
python -m compileall ai_utm_qa_agent rag_campaign_insight_agent anomaly_pacing_agent
```

---

## 6. Reporting Issues

When submitting an issue, include:

- A clear description of the problem  
- Steps to reproduce  
- Expected vs actual behavior  
- Any relevant logs or screenshots  

This helps maintainers diagnose problems quickly.

---

## 7. Code of Conduct

All contributors must follow the project Code of Conduct.  
Be respectful, collegial, and constructive.

---

## 8. License

By contributing, you agree that your contributions will be licensed under the MIT License of this repository.

---

If you have questions about contributing or design decisions, feel free to open a discussion thread.  
Thank you for helping improve this project!
