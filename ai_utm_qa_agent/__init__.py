"""AI UTM and Tag QA Agent.

Validates URLs and UTM parameters against a marketing taxonomy,
suggests fixes, and generates marketer-friendly QA summaries.
"""

from .utm_qa_agent import UTMQAAgent, UTMCheckResult, UTMCheckIssue

__all__ = ["UTMQAAgent", "UTMCheckResult", "UTMCheckIssue"]
