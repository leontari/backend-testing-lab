"""Tests for metrics exceptions."""
from __future__ import annotations

from shared.metrics.exceptions import (
    MetricConfigurationError,
    MetricNotFoundError,
    MetricRegistrationError,
    MetricsError,
)


def test_all_metric_errors_are_metrics_error() -> None:
    assert issubclass(MetricConfigurationError, MetricsError)
    assert issubclass(MetricNotFoundError, MetricsError)
    assert issubclass(MetricRegistrationError, MetricsError)


def test_metrics_error_is_runtime_error() -> None:
    assert issubclass(MetricsError, RuntimeError)


def test_exception_can_be_raised() -> None:
    msg = "Invalid metric"
    try:
        raise MetricConfigurationError(msg)
    except MetricsError as exc:
        assert str(exc) == msg  # noqa: PT017
