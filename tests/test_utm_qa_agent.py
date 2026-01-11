"""Tests for the UTM QA Agent."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_utm_qa_agent import UTMQAAgent, UTMCheckResult, UTMCheckIssue


class TestUTMQAAgent:
    """Tests for UTMQAAgent class."""

    @pytest.fixture
    def agent(self):
        """Create a UTMQAAgent instance."""
        return UTMQAAgent()

    def test_parse_full_url(self, agent):
        """Test parsing a full URL with UTM parameters."""
        url = "https://example.com/page?utm_source=email&utm_medium=email&utm_campaign=fy25_test"
        normalized, params = agent.parse_url_or_params(url)

        assert "example.com" in normalized
        assert params["utm_source"] == "email"
        assert params["utm_medium"] == "email"
        assert params["utm_campaign"] == "fy25_test"

    def test_parse_query_string_only(self, agent):
        """Test parsing a query string without full URL."""
        query = "utm_source=google&utm_medium=cpc&utm_campaign=fy25_brand"
        normalized, params = agent.parse_url_or_params(query)

        assert params["utm_source"] == "google"
        assert params["utm_medium"] == "cpc"

    def test_guess_channel_email(self, agent):
        """Test channel guessing for email source."""
        params = {"utm_source": "email", "utm_medium": "email"}
        channel = agent.guess_channel(params)
        assert channel == "email"

    def test_check_required_params_missing(self, agent):
        """Test detection of missing required parameters."""
        params = {"utm_source": "email"}  # Missing utm_medium and utm_campaign
        issues = agent.check_required_params(params)

        assert len(issues) >= 2
        assert any(i.param == "utm_medium" for i in issues)
        assert any(i.param == "utm_campaign" for i in issues)

    def test_check_allowed_values_invalid_source(self, agent):
        """Test detection of invalid utm_source values."""
        params = {"utm_source": "invalid_source", "utm_medium": "email"}
        issues = agent.check_allowed_values(params)

        assert any(i.param == "utm_source" for i in issues)

    @patch("ai_utm_qa_agent.utm_qa_agent.call_llm")
    def test_run_check_valid_url(self, mock_llm, agent):
        """Test full check on a valid URL."""
        mock_llm.return_value = "All parameters are valid."

        url = "https://example.com/?utm_source=email&utm_medium=email&utm_campaign=fy25_welcome"
        result = agent.run_check(url)

        assert isinstance(result, UTMCheckResult)
        assert result.channel_guess == "email"
        assert result.is_pass  # No errors expected


class TestUTMCheckIssue:
    """Tests for UTMCheckIssue dataclass."""

    def test_create_issue(self):
        """Test creating a UTMCheckIssue."""
        issue = UTMCheckIssue(
            type="missing_param",
            param="utm_source",
            message="Missing required parameter: utm_source",
            severity="error",
        )

        assert issue.type == "missing_param"
        assert issue.severity == "error"
