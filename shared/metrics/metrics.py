"""
Public metrics API.

This module exposes the only interface that the application code should use.

The implementation hides:
- prometheus_client;
- metric registration;
- backend lifecycle;
- metric caching.

Example:
-------
    metrics = Metrics()

    metrics.increment(
        "orders.created.total"
    )

    with metrics.timer(
        "database.query.seconds"
    ):
        repository.load()

"""

from __future__ import annotations

from dataclasses import dataclass, field

from shared.metrics.config import MetricsConfig
from shared.metrics.manager import MetricManager
from shared.metrics.prometheus import PrometheusBackend
from shared.metrics.timer import MetricTimer


def _create_metric_manager() -> MetricManager:
    """
    Create default metric manager.

    Factory function is used by dataclass default_factory to keep
    construction explicit and testable.

    Returns
    -------
        Initialized PrometheusBackend object

    """
    return MetricManager(PrometheusBackend())


@dataclass(slots=True, frozen=True)
class Metrics:
    """
    Application metrics facade.

    This object should normally be registered as singleton
    in the dependency injection container.

    Responsibilities:
    - provide simple metrics API;
    - delegate metric lifecycle to MetricManager;
    - hide backend implementation.

    It does not:
    - store metric values;
    - export metrics;
    - know about Prometheus endpoints.
    """

    manager: MetricManager = field(default_factory=_create_metric_manager)

    def increment(
        self,
        name: str,
        value: float = 1,
        *,
        description: str = "",
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Increment counter metric.

        Parameters
        ----------
        name:
            Metric name.
        value:
            Increment value.
        description:
            Metric description.
        labels:
            Optional metric labels.

        Example
        -------
            metrics.increment("orders.created.total")

        """
        metric = self.manager.counter(
            name=name,
            description=description,
            labels=self._labels(labels),
        )
        if labels:
            metric.labels(**labels).inc(value)
        else:
            metric.inc(value)

    def gauge(
        self,
        name: str,
        value: float,
        *,
        labels: dict[str, str] | None = None,
        description: str = "",
    ) -> None:
        """
        Set gauge value.

        Example:
        -------
            metrics.gauge("active.connections", 10)

        """
        metric = self.manager.gauge(
            name=name,
            description=description,
            labels=self._labels(labels),
        )
        if labels:
            metric.labels(**labels).set(value)
        else:
            metric.set(value)

    def observe(
        self,
        name: str,
        value: float,
        *,
        description: str = "",
        labels: dict[str, str] | None = None,
    ) -> None:
        """
        Observe histogram value.

        Example:
        -------
            metrics.observe("http.duration.seconds", 0.25)

        """
        metric = self.manager.histogram(
            name=name,
            description=description,
            labels=self._labels(labels),
        )
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)

    def timer(
        self,
        name: str,
        *,
        description: str = "",
        labels: dict[str, str] | None = None,
    ) -> MetricTimer:
        """
        Create execution timer.

        Supports:
            with metrics.timer(...):
                ...

            async with metrics.timer(...):
                ...

        Returns:
             Prometheus Histogram.time() context manager wrapper

        """
        histogram = self.manager.histogram(
            name=name,
            description=description,
            labels=self._labels(labels),
        )
        if labels:
            histogram = histogram.labels(**labels)

        return MetricTimer(histogram)

    @staticmethod
    def _labels(labels: dict[str, str] | None) -> tuple[str, ...]:
        """
        Convert runtime labels to Prometheus label names.

        Parameters
        ----------
        labels:
            Runtime metric labels mapping where keys represent
            Prometheus label names and values represent label values.

        Returns
        -------
            Tuple containing Prometheus label names extracted from the input
            mapping keys. Return an empty tuple when labels are not provided.

        """
        if not labels:
            return ()

        return tuple(labels.keys())


__all__ = ("Metrics",)
