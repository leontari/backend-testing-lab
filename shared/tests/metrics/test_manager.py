from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

import pytest
from prometheus_client import Counter

from shared.metrics.exceptions import (
    MetricConfigurationError,
    MetricNotFoundError,
    MetricRegistrationError,
)

if TYPE_CHECKING:
    from shared.metrics.manager import MetricManager


def test_counter_creates_metric(manager: MetricManager) -> None:
    """Counter should be created through backend."""
    metric = manager.counter(
        "orders_total",
        "Orders count",
    )

    assert isinstance(metric, Counter)


def test_counter_returns_cached_instance(manager: MetricManager) -> None:
    """Repeated registration should return same object."""
    first = manager.counter("orders_total")
    second = manager.counter("orders_total")

    assert first is second
    assert len(manager._types) == 1


def test_metric_type_cannot_change(manager: MetricManager) -> None:
    """Same metric name cannot be registered with another type."""
    manager.counter("request_metric")

    with pytest.raises(MetricRegistrationError):
        manager.histogram("request_metric")


def test_get_existing_metric(manager: MetricManager) -> None:
    """
    get() returns registered metric.
    """
    metric = manager.counter("orders_total")

    assert manager.get("orders_total") is metric


def test_get_missing_metric_returns_none(manager: MetricManager) -> None:
    """
    get() should not raise for missing metric.
    """

    assert manager.get("missing") is None


def test_require_missing_metric_raises(manager: MetricManager) -> None:
    """
    require() should raise when metric does not exist.
    """
    with pytest.raises(MetricNotFoundError):
        manager.require("missing")


def test_metric_type_returns_registered_type(manager: MetricManager) -> None:
    """
    metric_type() should return actual metric class.
    """
    manager.counter("orders_total")

    assert manager.metric_type("orders_total") is Counter


def test_empty_metric_name_is_invalid(manager: MetricManager) -> None:
    """
    Empty names should be rejected.
    """

    with pytest.raises(MetricConfigurationError):
        manager.counter("")


def test_whitespace_metric_name_is_invalid(manager: MetricManager) -> None:
    """
    Whitespace names should be rejected.
    """
    with pytest.raises(MetricConfigurationError):
        manager.counter("   ")


def test_duplicate_labels_are_invalid(manager: MetricManager) -> None:
    """
    Labels must be unique.
    """

    with pytest.raises(MetricConfigurationError):
        manager.counter(
            "request_total",
            labels=("method", "method"),
        )


def test_labels_are_passed_to_backend(
    manager: MetricManager,
) -> None:
    """
    Labels should be accepted and preserved.
    """
    metric = manager.counter(
        "request_total",
        labels=("method",),
    )

    assert isinstance(metric, Counter)


def test_concurrent_creation_is_safe(manager: MetricManager) -> None:
    """
    Concurrent creation must produce one metric instance.
    """
    results: list[object] = []

    def worker() -> None:
        results.append(manager.counter("concurrent_metric"))

    threads = [Thread(target=worker) for _ in range(20)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(results) == 20
    assert all(item is results[0] for item in results)
    assert len(manager._types) == 1
