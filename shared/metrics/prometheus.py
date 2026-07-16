"""
Prometheus metrics backend.

This module contains integration with prometheus_client.

Responsibilities:
- create Prometheus metric objects;
- configure backend-specific options;
- hide prometheus_client implementation details.

This module MUST NOT be imported by application code directly.

Application code should use:
    from metrics import Metrics
instead.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram

if TYPE_CHECKING:
    from shared.metrics.config import MetricsConfig


@dataclass(slots=True, frozen=True)
class PrometheusBackend:
    """
    Prometheus metrics backend adapter.

    The backend owns Prometheus-specific configuration.

    Responsibilities:
    - create metric primitives;
    - apply namespace;
    - apply histogram buckets;
    - isolate collector registry.

    It does not:
    - store application metrics;
    - manage lifecycle;
    - expose public metrics API.

    """

    config: MetricsConfig = field(default_factory=MetricsConfig)
    registry: CollectorRegistry = field(default_factory=CollectorRegistry)

    def create_counter(
        self,
        name: str,
        description: str,
        labels: tuple[str, ...] = (),
    ) -> Counter:
        """
        Create Prometheus counter.

        Parameters
        ----------
        name:
            Metric name.
        description:
            Human-readable metric description.
        labels:
            Label names.

        Returns
        -------
        Counter
            Prometheus counter instance.

        """
        return Counter(
            name=name,
            documentation=description,
            labelnames=labels,
            namespace=self.config.namespace,
            registry=self.registry,
        )

    def create_gauge(
        self,
        name: str,
        description: str,
        labels: tuple[str, ...] = (),
    ) -> Gauge:
        """
        Create Prometheus gauge.

        Parameters
        ----------
        name:
            Metric name.
        description:
            Human-readable metric description.
        labels:
            Label names.

        Returns
        -------
        Gauge
            Prometheus gauge instance.

        """
        return Gauge(
            name=name,
            documentation=description,
            labelnames=labels,
            namespace=self.config.namespace,
            registry=self.registry,
        )

    def create_histogram(
        self,
        name: str,
        description: str,
        labels: tuple[str, ...] = (),
    ) -> Histogram:
        """
        Create Prometheus histogram.

        Parameters
        ----------
        name:
            Metric name.

        description:
            Human-readable metric description.

        labels:
            Label names.

        Returns
        -------
        Histogram
            Prometheus histogram instance.

        """
        return Histogram(
            name=name,
            documentation=description,
            labelnames=labels,
            namespace=self.config.namespace,
            buckets=self.config.histogram_buckets,
            registry=self.registry,
        )


__all__ = ("PrometheusBackend",)
