"""Tests for the Anomaly and Pacing Monitoring Agent."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from anomaly_pacing_agent import AnomalyDetector, DailyMetrics, Anomaly


class TestDailyMetrics:
    """Tests for DailyMetrics dataclass."""

    def test_cpc_calculation(self):
        """Test cost per click calculation."""
        metrics = DailyMetrics(day=1, channel="email", spend=100.0, clicks=50, conversions=5)
        assert metrics.cpc == 2.0

    def test_cpc_zero_clicks(self):
        """Test CPC when clicks is zero."""
        metrics = DailyMetrics(day=1, channel="email", spend=100.0, clicks=0, conversions=0)
        assert metrics.cpc == 0.0

    def test_ctr_calculation(self):
        """Test click-through rate calculation."""
        metrics = DailyMetrics(day=1, channel="email", spend=100.0, clicks=100, conversions=10)
        # CTR = clicks / (clicks * 10) = 0.1
        assert metrics.ctr == 0.1

    def test_cvr_calculation(self):
        """Test conversion rate calculation."""
        metrics = DailyMetrics(day=1, channel="email", spend=100.0, clicks=100, conversions=5)
        assert metrics.cvr == 0.05

    def test_cpa_calculation(self):
        """Test cost per acquisition calculation."""
        metrics = DailyMetrics(day=1, channel="email", spend=100.0, clicks=50, conversions=5)
        assert metrics.cpa == 20.0


class TestAnomalyDetector:
    """Tests for AnomalyDetector class."""

    @pytest.fixture
    def detector(self):
        """Create an AnomalyDetector with standard thresholds."""
        return AnomalyDetector(
            daily_budget=1000.0,
            max_cpa=100.0,
            min_ctr=0.02,
            min_cvr=0.03,
        )

    def test_detect_overspend(self, detector):
        """Test detection of overspend anomaly."""
        metrics = [
            DailyMetrics(day=1, channel="paid_search", spend=1300.0, clicks=100, conversions=10),
        ]
        anomalies = detector.detect(metrics)

        assert any(a.metric == "spend" and a.direction == "up" for a in anomalies)

    def test_detect_underspend(self, detector):
        """Test detection of underspend anomaly."""
        metrics = [
            DailyMetrics(day=1, channel="paid_search", spend=500.0, clicks=50, conversions=5),
        ]
        anomalies = detector.detect(metrics)

        assert any(a.metric == "spend" and a.direction == "down" for a in anomalies)

    def test_detect_high_cpa(self, detector):
        """Test detection of CPA above guardrail."""
        metrics = [
            DailyMetrics(day=1, channel="paid_search", spend=1000.0, clicks=50, conversions=5),
            # CPA = 1000 / 5 = 200, above max_cpa of 100
        ]
        anomalies = detector.detect(metrics)

        assert any(a.metric == "cpa" for a in anomalies)

    def test_no_anomalies_normal_performance(self, detector):
        """Test no anomalies for normal performance."""
        metrics = [
            DailyMetrics(day=1, channel="email", spend=950.0, clicks=100, conversions=10),
            # Spend within 25% of budget, good CPA, good CVR
        ]
        anomalies = detector.detect(metrics)

        # Should only have anomalies if thresholds are breached
        spend_anomalies = [a for a in anomalies if a.metric == "spend"]
        assert len(spend_anomalies) == 0


class TestAnomaly:
    """Tests for Anomaly dataclass."""

    def test_create_anomaly(self):
        """Test creating an Anomaly."""
        anomaly = Anomaly(
            day=1,
            channel="paid_search",
            metric="spend",
            value=1500.0,
            baseline=1000.0,
            deviation_pct=50.0,
            direction="up",
            severity="critical",
            reason="Spend is above daily budget target.",
        )

        assert anomaly.metric == "spend"
        assert anomaly.severity == "critical"
        assert anomaly.deviation_pct == 50.0
