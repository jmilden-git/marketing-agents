"""AI Anomaly and Pacing Monitoring Agent.

Monitors multi-channel campaign performance, detects anomalies,
and produces structured alerts plus narrative commentary.
"""

from .anomaly_pacing_agent import (
    AnomalyDetector,
    AnomalyReportingAgent,
    DailyMetrics,
    Anomaly,
)

__all__ = ["AnomalyDetector", "AnomalyReportingAgent", "DailyMetrics", "Anomaly"]
