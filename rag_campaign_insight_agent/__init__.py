"""RAG Campaign Insight Agent.

Uses retrieval-augmented generation to find similar past campaigns
and synthesize insights, recommendations, and KPI risk callouts.
"""

from .rag_campaign_insight_agent import (
    RAGCampaignInsightAgent,
    CampaignCorpus,
    Campaign,
)

__all__ = ["RAGCampaignInsightAgent", "CampaignCorpus", "Campaign"]
