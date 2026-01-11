"""Tests for the RAG Campaign Insight Agent."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rag_campaign_insight_agent import Campaign, CampaignCorpus, RAGCampaignInsightAgent


class TestCampaign:
    """Tests for Campaign dataclass."""

    def test_create_campaign(self):
        """Test creating a Campaign."""
        campaign = Campaign(
            id="C001",
            name="Q1 Email Launch",
            channel="email",
            audience="enterprise",
            objective="lead_generation",
            kpis={"open_rate": 0.25, "click_rate": 0.05},
            summary="Enterprise email campaign for Q1 product launch.",
        )

        assert campaign.id == "C001"
        assert campaign.channel == "email"
        assert campaign.kpis["open_rate"] == 0.25


class TestCampaignCorpus:
    """Tests for CampaignCorpus class."""

    @pytest.fixture
    def sample_campaigns(self):
        """Create sample campaigns for testing."""
        return [
            Campaign(
                id="C001",
                name="Email Nurture Series",
                channel="email",
                audience="mid_market",
                objective="nurture",
                kpis={"open_rate": 0.30, "click_rate": 0.08},
                summary="Email nurture campaign targeting mid-market prospects.",
            ),
            Campaign(
                id="C002",
                name="Paid Search Brand",
                channel="paid_search",
                audience="enterprise",
                objective="acquisition",
                kpis={"ctr": 0.05, "conversion_rate": 0.03},
                summary="Paid search campaign for enterprise brand keywords.",
            ),
            Campaign(
                id="C003",
                name="Social Awareness",
                channel="paid_social",
                audience="smb",
                objective="awareness",
                kpis={"ctr": 0.02, "cpl": 45.0},
                summary="Social media awareness campaign for SMB segment.",
            ),
        ]

    def test_corpus_creation(self, sample_campaigns):
        """Test creating a CampaignCorpus."""
        corpus = CampaignCorpus(sample_campaigns)

        assert len(corpus.campaigns) == 3
        assert corpus.matrix is not None

    def test_most_similar_returns_correct_count(self, sample_campaigns):
        """Test that most_similar returns the requested number of results."""
        corpus = CampaignCorpus(sample_campaigns)
        brief = "Looking for email marketing insights"

        similar = corpus.most_similar(brief, top_n=2)

        assert len(similar) == 2
        assert all(isinstance(item, tuple) for item in similar)
        assert all(isinstance(item[0], Campaign) for item in similar)
        assert all(isinstance(item[1], float) for item in similar)

    def test_most_similar_ranks_by_relevance(self, sample_campaigns):
        """Test that similar campaigns are ranked by relevance."""
        corpus = CampaignCorpus(sample_campaigns)
        brief = "email nurture campaign for mid market"

        similar = corpus.most_similar(brief, top_n=3)

        # Email campaign should be most similar to email brief
        top_campaign, top_score = similar[0]
        assert top_campaign.channel == "email"


class TestRAGCampaignInsightAgent:
    """Tests for RAGCampaignInsightAgent class."""

    @pytest.fixture
    def agent(self, tmp_path):
        """Create a RAGCampaignInsightAgent with test data."""
        # Create test campaign history
        campaign_history = [
            {
                "id": "C001",
                "name": "Test Campaign",
                "channel": "email",
                "audience": "enterprise",
                "objective": "acquisition",
                "kpis": {"open_rate": 0.25},
                "summary": "Test email campaign.",
            }
        ]
        history_path = tmp_path / "campaign_history.json"
        history_path.write_text(json.dumps(campaign_history))

        # Create test KPI dictionary
        kpi_dict = {
            "open_rate": "Email open rate metric",
            "click_rate": "Email click-through rate",
        }
        kpi_path = tmp_path / "kpi_dictionary.yaml"
        kpi_path.write_text("open_rate: Email open rate metric\nclick_rate: Email click-through rate\n")

        return RAGCampaignInsightAgent(history_path, kpi_path)

    def test_build_prompt_includes_brief(self, agent):
        """Test that build_prompt includes the campaign brief."""
        brief = "New email campaign targeting SMB"
        similar = agent.corpus.most_similar(brief, top_n=1)

        prompt = agent.build_prompt(brief, similar)

        assert "New email campaign targeting SMB" in prompt
        assert "marketing analytics strategist" in prompt.lower()

    @patch("rag_campaign_insight_agent.rag_campaign_insight_agent.call_llm")
    def test_generate_insight_calls_llm(self, mock_llm, agent):
        """Test that generate_insight calls the LLM."""
        mock_llm.return_value = "Based on similar campaigns, here are insights..."

        brief = "Plan a new email campaign"
        insight = agent.generate_insight(brief)

        mock_llm.assert_called_once()
        assert insight == "Based on similar campaigns, here are insights..."
