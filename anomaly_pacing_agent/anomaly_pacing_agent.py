import random
import statistics
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for shared imports when running as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared import call_llm

@dataclass
class DailyMetrics:
    day: int
    channel: str
    spend: float
    clicks: int
    conversions: int

    @property
    def cpc(self) -> float:
        return self.spend / self.clicks if self.clicks > 0 else 0.0

    @property
    def ctr(self) -> float:
        # Assume 10 times clicks as impressions for this simple sim
        impressions = self.clicks * 10
        return self.clicks / impressions if impressions > 0 else 0.0

    @property
    def cvr(self) -> float:
        return self.conversions / self.clicks if self.clicks > 0 else 0.0

    @property
    def cpa(self) -> float:
        return self.spend / self.conversions if self.conversions > 0 else 0.0


@dataclass
class Anomaly:
    day: int
    channel: str
    metric: str
    value: float
    baseline: float
    deviation_pct: float
    direction: str  # "up" or "down"
    severity: str   # "info", "warning", "critical"
    reason: str


class AnomalyDetector:
    def __init__(self, daily_budget: float, max_cpa: float, min_ctr: float, min_cvr: float) -> None:
        self.daily_budget = daily_budget
        self.max_cpa = max_cpa
        self.min_ctr = min_ctr
        self.min_cvr = min_cvr

    def detect(self, metrics: List[DailyMetrics]) -> List[Anomaly]:
        anomalies: List[Anomaly] = []

        spend_values = [m.spend for m in metrics]
        cpa_values = [m.cpa for m in metrics if m.conversions > 0]
        ctr_values = [m.ctr for m in metrics if m.clicks > 0]
        cvr_values = [m.cvr for m in metrics if m.clicks > 0]

        spend_avg = statistics.mean(spend_values)
        cpa_avg = statistics.mean(cpa_values) if cpa_values else 0.0
        ctr_avg = statistics.mean(ctr_values) if ctr_values else 0.0
        cvr_avg = statistics.mean(cvr_values) if cvr_values else 0.0

        for m in metrics:
            # Spend pacing
            if m.spend > self.daily_budget * 1.25:
                deviation_pct = (m.spend - self.daily_budget) / self.daily_budget * 100
                anomalies.append(
                    Anomaly(
                        day=m.day,
                        channel=m.channel,
                        metric="spend",
                        value=m.spend,
                        baseline=self.daily_budget,
                        deviation_pct=deviation_pct,
                        direction="up",
                        severity="warning" if deviation_pct < 50 else "critical",
                        reason="Spend is above daily budget target.",
                    )
                )
            elif m.spend < self.daily_budget * 0.75:
                deviation_pct = (self.daily_budget - m.spend) / self.daily_budget * 100
                anomalies.append(
                    Anomaly(
                        day=m.day,
                        channel=m.channel,
                        metric="spend",
                        value=m.spend,
                        baseline=self.daily_budget,
                        deviation_pct=deviation_pct,
                        direction="down",
                        severity="info",
                        reason="Spend is below pacing target.",
                    )
                )

            # CPA guardrail
            if m.conversions > 0 and m.cpa > self.max_cpa:
                deviation_pct = (m.cpa - self.max_cpa) / self.max_cpa * 100
                anomalies.append(
                    Anomaly(
                        day=m.day,
                        channel=m.channel,
                        metric="cpa",
                        value=m.cpa,
                        baseline=self.max_cpa,
                        deviation_pct=deviation_pct,
                        direction="up",
                        severity="critical",
                        reason="CPA above guardrail threshold.",
                    )
                )

            # CTR relative anomaly
            if m.clicks > 0 and m.ctr < ctr_avg * 0.7:
                deviation_pct = (ctr_avg - m.ctr) / ctr_avg * 100 if ctr_avg > 0 else 0
                anomalies.append(
                    Anomaly(
                        day=m.day,
                        channel=m.channel,
                        metric="ctr",
                        value=m.ctr,
                        baseline=ctr_avg,
                        deviation_pct=deviation_pct,
                        direction="down",
                        severity="warning",
                        reason="CTR significantly below rolling average.",
                    )
                )

            # CVR guardrail
            if m.clicks > 0 and m.cvr < self.min_cvr:
                deviation_pct = (self.min_cvr - m.cvr) / self.min_cvr * 100
                anomalies.append(
                    Anomaly(
                        day=m.day,
                        channel=m.channel,
                        metric="cvr",
                        value=m.cvr,
                        baseline=self.min_cvr,
                        deviation_pct=deviation_pct,
                        direction="down",
                        severity="warning",
                        reason="Conversion rate below minimum target.",
                    )
                )

        return anomalies


class AnomalyReportingAgent:
    def __init__(self, detector: AnomalyDetector) -> None:
        self.detector = detector

    def explain_anomalies(self, anomalies: List[Anomaly]) -> str:
        if not anomalies:
            return "No material anomalies detected. Campaign pacing and efficiency are within guardrails."

        bullets = []
        for a in anomalies:
            bullets.append(
                f"- Day {a.day}, {a.channel}: {a.metric.upper()} is {a.deviation_pct:.1f}% "
                f"{'above' if a.direction == 'up' else 'below'} baseline. {a.reason}"
            )

        anomalies_text = "\n".join(bullets)

        prompt = f"""
You are a performance marketing manager. You received the following anomaly summary:

{anomalies_text}

Write:
1. A short executive summary (2 to 3 sentences).
2. Three recommended actions with clear priorities.
3. A note on what to monitor for the next 48 hours.

Keep the tone practical and focused on decision making.
"""
        return call_llm(prompt)

    def build_slack_message(self, anomalies: List[Anomaly]) -> str:
        if not anomalies:
            return ":white_check_mark: Pacing check complete. No anomalies detected today."

        lines = [":warning: Daily Pacing and KPI Anomalies"]
        for a in anomalies:
            lines.append(
                f"- Day {a.day}, {a.channel}: {a.metric.upper()} {a.direction} "
                f"{a.deviation_pct:.1f}% vs baseline. {a.reason}"
            )
        return "\n".join(lines)


def generate_synthetic_metrics(days: int = 14) -> List[DailyMetrics]:
    channels = ["email", "paid_search", "paid_social"]
    metrics: List[DailyMetrics] = []

    for day in range(1, days + 1):
        for channel in channels:
            base_spend = 800 if channel == "email" else 1000 if channel == "paid_search" else 600
            spend = random.uniform(base_spend * 0.8, base_spend * 1.2)
            clicks = int(spend / random.uniform(1.0, 3.0))
            conversions = int(clicks * random.uniform(0.02, 0.08))

            # Inject a couple of anomalies
            if day == days and channel == "paid_search":
                spend *= 1.7  # Overspend
            if day == days - 1 and channel == "paid_social":
                conversions = max(1, int(conversions * 0.2))  # CVR drop

            metrics.append(
                DailyMetrics(
                    day=day,
                    channel=channel,
                    spend=round(spend, 2),
                    clicks=clicks,
                    conversions=conversions,
                )
            )

    return metrics


def demo():
    daily_budget = 1000.0
    max_cpa = 120.0
    min_ctr = 0.02
    min_cvr = 0.03

    metrics = generate_synthetic_metrics()
    detector = AnomalyDetector(daily_budget, max_cpa, min_ctr, min_cvr)
    anomalies = detector.detect(metrics)

    agent = AnomalyReportingAgent(detector)

    print("Sample anomalies JSON:")
    for a in anomalies:
        print(asdict(a))

    print("\nSlack style message:")
    print(agent.build_slack_message(anomalies))

    print("\nLLM narrative explanation:")
    print(agent.explain_anomalies(anomalies))


if __name__ == "__main__":
    demo()
