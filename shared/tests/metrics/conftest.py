from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from shared.metrics import Metrics
from shared.metrics.config import MetricsConfig
from shared.metrics.manager import MetricManager
from shared.metrics.prometheus import PrometheusBackend

if TYPE_CHECKING:
    from prometheus_client import Histogram


@pytest.fixture
def config() -> MetricsConfig:
    return MetricsConfig()


@pytest.fixture
def backend(config: MetricsConfig) -> PrometheusBackend:
    return PrometheusBackend(config)


@pytest.fixture
def manager(backend: PrometheusBackend) -> MetricManager:
    return MetricManager(backend)


class FakeTimer:
    def __init__(self):
        self.entered = False
        self.exited = False

    def __enter__(self):
        self.entered = True

    def __exit__(self, exc_type, exc, tb):
        self.exited = True


@pytest.fixture
def histogram() -> Histogram:
    histogram = Mock()
    histogram.time.return_value = FakeTimer()

    return histogram
