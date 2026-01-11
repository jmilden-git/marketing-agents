import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Add parent directory to path for shared imports when running as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared import call_llm


@dataclass
class Campaign:
    id: str
    name: str
    channel: str
    audience: str
    objective: str
    kpis: Dict[str, float]
    summary: str


class CampaignCorpus:
    def __init__(self, campaigns: List[Campaign]) -> None:
        self.campaigns = campaigns
        self.vectorizer = TfidfVectorizer()
        texts = [self._campaign_text(c) for c in campaigns]
        self.matrix = self.vectorizer.fit_transform(texts)

    @staticmethod
    def _campaign_text(c: Campaign) -> str:
        return (
            f"{c.name} {c.channel} {c.audience} {c.objective} "
            f"{json.dumps(c.kpis)} {c.summary}"
        )

    def most_similar(self, brief_text: str, top_n: int = 3) -> List[Tuple[Campaign, float]]:
        query_vec = self.vectorizer.transform([brief_text])
        sims = cosine_similarity(query_vec, self.matrix).flatten()
        ranked_indices = sims.argsort()[::-1][:top_n]
        return [(self.campaigns[i], float(sims[i])) for i in ranked_indices]


class RAGCampaignInsightAgent:
    def __init__(self, campaign_history_path: Path, kpi_dict_path: Path) -> None:
        with campaign_history_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        self.corpus = CampaignCorpus(
            campaigns=[
                Campaign(
                    id=item["id"],
                    name=item["name"],
                    channel=item["channel"],
                    audience=item["audience"],
                    objective=item["objective"],
                    kpis=item["kpis"],
                    summary=item["summary"],
                )
                for item in raw
            ]
        )

        with kpi_dict_path.open("r", encoding="utf-8") as f:
            self.kpi_dict = yaml.safe_load(f)

    def build_prompt(
        self,
        brief: str,
        similar_campaigns: List[Tuple[Campaign, float]],
    ) -> str:
        lines = []
        lines.append("You are a marketing analytics strategist.")
        lines.append("You will analyze a new campaign brief using similar past campaigns.")
        lines.append("")
        lines.append("New campaign brief:")
        lines.append(brief)
        lines.append("")
        lines.append("Relevant past campaigns:")
        for campaign, score in similar_campaigns:
            lines.append(f"- ID: {campaign.id} (similarity {score:.2f})")
            lines.append(f"  Name: {campaign.name}")
            lines.append(f"  Channel: {campaign.channel}")
            lines.append(f"  Audience: {campaign.audience}")
            lines.append(f"  Objective: {campaign.objective}")
            lines.append(f"  KPIs: {campaign.kpis}")
            lines.append(f"  Summary: {campaign.summary}")
            lines.append("")
        lines.append("KPI dictionary:")
        for kpi, desc in self.kpi_dict.items():
            lines.append(f"- {kpi}: {desc}")
        lines.append("")
        lines.append("Tasks:")
        lines.append("1. Summarize the main pattern across the similar campaigns.")
        lines.append("2. Suggest three specific recommendations for this new campaign.")
        lines.append("3. Call out any KPI risks or tradeoffs to monitor.")
        lines.append("Return a concise answer suitable for an internal GTM update.")
        return "\n".join(lines)

    def generate_insight(self, brief: str) -> str:
        similar_campaigns = self.corpus.most_similar(brief, top_n=3)
        prompt = self.build_prompt(brief, similar_campaigns)
        return call_llm(prompt)

    def demo(self) -> None:
        brief = (
            "Plan a mid market free trial acquisition campaign using paid search and email nurture. "
            "Primary objective is trial sign ups and secondary objective is activation into paid plans. "
            "Budget is constrained so we care a lot about CPL and conversion rate."
        )
        insight = self.generate_insight(brief)
        print("New brief:")
        print(brief)
        print("\nInsight:")
        print(insight)


if __name__ == "__main__":
    default_history = Path(__file__).with_name("campaign_history.json")
    default_kpis = Path(__file__).with_name("kpi_dictionary.yaml")

    parser = argparse.ArgumentParser(
        description="Generate a quick insight summary for a campaign brief using RAG-style lookup."
    )
    parser.add_argument(
        "brief",
        nargs="?",
        help="Campaign brief text. If omitted, a demo brief is used.",
    )
    parser.add_argument(
        "--history",
        type=Path,
        default=default_history,
        help=f"Path to campaign history JSON (default: {default_history.name})",
    )
    parser.add_argument(
        "--kpis",
        type=Path,
        default=default_kpis,
        help=f"Path to KPI dictionary YAML (default: {default_kpis.name})",
    )

    args = parser.parse_args()
    agent = RAGCampaignInsightAgent(args.history, args.kpis)

    if args.brief:
        print(agent.generate_insight(args.brief))
    else:
        agent.demo()
