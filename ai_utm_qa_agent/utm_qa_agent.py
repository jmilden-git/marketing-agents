import json
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for shared imports when running as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared import call_llm

@dataclass
class UTMCheckIssue:
    type: str
    param: Optional[str]
    message: str
    severity: str  # "error", "warning", "info"


@dataclass
class UTMCheckResult:
    original_url: str
    normalized_url: str
    issues: List[UTMCheckIssue]
    channel_guess: Optional[str]
    is_pass: bool
    suggested_url: Optional[str]
    explanation: str


class UTMQAAgent:
    def __init__(self, taxonomy_path: str = "utm_taxonomy.json") -> None:
        resolved_path = Path(taxonomy_path)
        if not resolved_path.is_absolute():
            resolved_path = Path(__file__).resolve().parent / resolved_path

        if not resolved_path.is_file():
            raise FileNotFoundError(f"Taxonomy file not found at {resolved_path}")

        with resolved_path.open("r", encoding="utf-8") as f:
            self.taxonomy = json.load(f)

    def parse_url_or_params(self, input_str: str) -> Tuple[str, Dict[str, str]]:
        """
        Accepts either a full URL or a query-string style param block.
        Returns normalized URL and params dict.
        """
        input_str = input_str.strip()
        if "http://" in input_str or "https://" in input_str:
            parsed = urllib.parse.urlparse(input_str)
            params = dict(urllib.parse.parse_qsl(parsed.query))
            normalized = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(params)))
            return normalized, params
        else:
            # Assume query string block like "utm_source=email&utm_medium=email"
            params = dict(urllib.parse.parse_qsl(input_str))
            normalized = "https://example.com/landing-page?" + urllib.parse.urlencode(params)
            return normalized, params

    def guess_channel(self, params: Dict[str, str]) -> Optional[str]:
        source = params.get("utm_source", "").lower()
        if source in self.taxonomy["channel_defaults"]:
            return source
        medium = params.get("utm_medium", "").lower()
        for channel, defaults in self.taxonomy["channel_defaults"].items():
            if medium == defaults.get("utm_medium"):
                return channel
        return None

    def check_required_params(self, params: Dict[str, str]) -> List[UTMCheckIssue]:
        issues: List[UTMCheckIssue] = []
        for req in self.taxonomy["required_params"]:
            if req not in params or not params[req]:
                issues.append(
                    UTMCheckIssue(
                        type="missing_param",
                        param=req,
                        message=f"Missing required parameter: {req}",
                        severity="error",
                    )
                )
        return issues

    def check_allowed_values(self, params: Dict[str, str]) -> List[UTMCheckIssue]:
        issues: List[UTMCheckIssue] = []
        allowed = self.taxonomy["allowed_values"]
        utm_source = params.get("utm_source", "").lower()
        utm_medium = params.get("utm_medium", "").lower()
        utm_campaign = params.get("utm_campaign", "")

        if utm_source and utm_source not in allowed["utm_source"]:
            issues.append(
                UTMCheckIssue(
                    type="invalid_value",
                    param="utm_source",
                    message=f"utm_source '{utm_source}' is not in allowed list {allowed['utm_source']}",
                    severity="warning",
                )
            )

        if utm_medium and utm_medium not in allowed["utm_medium"]:
            issues.append(
                UTMCheckIssue(
                    type="invalid_value",
                    param="utm_medium",
                    message=f"utm_medium '{utm_medium}' is not in allowed list {allowed['utm_medium']}",
                    severity="warning",
                )
            )

        if utm_campaign and allowed["utm_campaign_prefixes"]:
            if not any(utm_campaign.startswith(prefix) for prefix in allowed["utm_campaign_prefixes"]):
                issues.append(
                    UTMCheckIssue(
                        type="naming_convention",
                        param="utm_campaign",
                        message=(
                            f"utm_campaign '{utm_campaign}' does not start with any allowed prefix "
                            f"{allowed['utm_campaign_prefixes']}"
                        ),
                        severity="info",
                    )
                )

        return issues

    def build_suggested_params(self, params: Dict[str, str], channel_guess: Optional[str]) -> Dict[str, str]:
        updated = params.copy()
        if channel_guess and channel_guess in self.taxonomy["channel_defaults"]:
            defaults = self.taxonomy["channel_defaults"][channel_guess]
            for key, val in defaults.items():
                if not updated.get(key):
                    updated[key] = val
        return updated

    def build_explanation(self, issues: List[UTMCheckIssue], suggested_url: Optional[str]) -> str:
        issue_lines = []
        for issue in issues:
            issue_lines.append(f"- [{issue.severity.upper()}] {issue.message}")

        issues_text = "\n".join(issue_lines) if issue_lines else "No issues detected."

        prompt = f"""
You are a marketing operations specialist. Summarize this UTM QA result in simple language.

Issues:
{issues_text}

Suggested URL: {suggested_url}

Provide:
1. A one paragraph summary for a marketer.
2. A short list of recommended next steps.
"""
        explanation = call_llm(prompt)
        return explanation

    def run_check(self, input_str: str) -> UTMCheckResult:
        normalized_url, params = self.parse_url_or_params(input_str)
        channel_guess = self.guess_channel(params)
        issues: List[UTMCheckIssue] = []
        issues.extend(self.check_required_params(params))
        issues.extend(self.check_allowed_values(params))

        suggested_params = self.build_suggested_params(params, channel_guess)
        suggested_url = normalized_url.split("?")[0] + "?" + urllib.parse.urlencode(suggested_params)

        is_pass = all(issue.severity != "error" for issue in issues)
        explanation = self.build_explanation(issues, suggested_url)

        return UTMCheckResult(
            original_url=input_str,
            normalized_url=normalized_url,
            issues=issues,
            channel_guess=channel_guess,
            is_pass=is_pass,
            suggested_url=suggested_url,
            explanation=explanation,
        )


def demo():
    agent = UTMQAAgent()
    test_inputs = [
        "https://example.com/demo?utm_source=email&utm_medium=email&utm_campaign=welcome_series",
        "utm_source=newsletter&utm_medium=email&utm_campaign=q1_launch",
        "https://example.com/?utm_medium=cpc&utm_campaign=search_brand",
    ]

    for url in test_inputs:
        result = agent.run_check(url)
        print("=" * 80)
        print("Original:", result.original_url)
        print("Normalized:", result.normalized_url)
        print("Channel guess:", result.channel_guess)
        print("Pass:", result.is_pass)
        print("Suggested URL:", result.suggested_url)
        print("Issues:")
        for issue in result.issues:
            print(f"  - ({issue.severity}) {issue.param}: {issue.message}")
        print("Explanation:")
        print(result.explanation)
        print("=" * 80)


if __name__ == "__main__":
    demo()
