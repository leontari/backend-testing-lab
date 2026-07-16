"""Tests for Metrics facade."""
from __future__ import annotations

from unittest.mock import Mock

import pytest

from shared.metrics.metrics import Metrics


@pytest.fixture
def manager() -> Mock:
    return Mock()


@pytest.fixture
def metrics(manager: Mock) -> Metrics:
    return Metrics(manager=manager)


def test_increment(metrics: Metrics, manager: Mock) -> None:
    counter = Mock()

    manager.counter.return_value = counter
    metrics.increment("orders.total")
    counter.inc.assert_called_once_with(1)


def test_gauge(metrics: Metrics, manager: Mock) -> None:
    gauge = Mock()

    manager.gauge.return_value = gauge
    metrics.gauge(
        "connections",
        5,
    )
    gauge.set.assert_called_once_with(5)


def test_observe(metrics: Metrics, manager: Mock) -> None:
    histogram = Mock()

    manager.histogram.return_value = histogram
    metrics.observe("request.duration", 0.1)
    histogram.observe.assert_called_once_with(0.1)


def test_timer(metrics: Metrics, manager: Mock) -> None:
    histogram = Mock()
    manager.histogram.return_value = histogram
    timer = metrics.timer("query.duration")

    assert timer is not None
