"""Common LLM integration utilities.

This module provides a unified interface for LLM calls across all agents.
The implementation can be easily swapped to use different providers.
"""

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore[assignment]


def call_llm(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.3,
    max_tokens: int = 400,
) -> str:
    """
    Call the LLM with the given prompt.

    Args:
        prompt: The prompt to send to the LLM.
        model: The model to use (default: gpt-4o-mini).
        temperature: Sampling temperature (default: 0.3 for deterministic outputs).
        max_tokens: Maximum tokens in response (default: 400).

    Returns:
        The LLM's response text.

    Raises:
        SystemExit: If OpenAI SDK is not installed or API key is missing.
    """
    if OpenAI is None:
        raise SystemExit(
            "Missing dependency: install OpenAI SDK with `pip install openai` or "
            "remove the OpenAI call in `call_llm`."
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY before running this script.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
