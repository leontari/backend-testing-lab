"""Tests for metrics package exports."""


def test_public_imports():
    from shared.metrics import (
        Metrics,
        MetricsError,
    )

    assert Metrics is not None
    assert MetricsError is not None
