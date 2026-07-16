"""
Metric manager.

This module manages lifecycle and registration of metric instances.

Responsibilities:
- lazy metric creation;
- metric instance caching;
- duplicate registration protection;
- metric type consistency.
- metric lookup;
- metric configuration validation.

The manager works through PrometheusBackend abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import TYPE_CHECKING, TypeVar, cast

from prometheus_client import Counter, Gauge, Histogram

from shared.metrics.exceptions import (
    MetricConfigurationError,
    MetricNotFoundError,
    MetricRegistrationError,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from shared.metrics.prometheus import PrometheusBackend


MetricT = TypeVar("MetricT", Counter, Gauge, Histogram)


@dataclass(slots=True)
class MetricManager:
    """
    Runtime metric registry manager.

    MetricManager stores created metric instances and guarantees
    that every metric name is registered only once with a single
    metric type.

    Normally this object should be created as a singleton and injected
    into Metrics facade.

    Responsibilities
    ----------------
    - metric instance ownership;
    - metric registration synchronization;
    - metric type consistency;
    - metric lookup.

    It does not:
    - expose application API;
    - manage metric export;
    - know about Prometheus scraping.

    """

    _backend: PrometheusBackend
    _metrics: dict[str, object] = field(init=False, default_factory=dict)
    _types: dict[str, type[object]] = field(init=False, default_factory=dict)
    _lock: RLock = field(init=False, default_factory=RLock)

    def counter(
        self,
        name: str,
        description: str = "",
        labels: tuple[str, ...] = ()
    ) -> Counter:
        """
        Get or create Counter metric.

        Parameters
        ----------
        name:
            Metric name.
        description:
            Human-readable metric description.
        labels:
            Label names attached to metric.

        Returns
        -------
        Counter
            Prometheus counter instance.

        """
        self._validate_labels(labels)

        return self._get_or_create(
            name=name,
            expected_type=Counter,
            factory=lambda: self._backend.create_counter(
                name=name,
                description=description,
                labels=labels,
            )
        )

    def gauge(
        self,
        name: str,
        description: str = "",
        labels: tuple[str, ...] = ()
    ) -> Gauge:
        """
        Get or create Gauge metric.

        Parameters
        ----------
        name:
            Metric name.
        description:
            Human-readable metric description.
        labels:
            Label names attached to metric.

        Returns
        -------
        Gauge
            Prometheus gauge instance.

        """
        self._validate_labels(labels)

        return self._get_or_create(
            name=name,
            expected_type=Gauge,
            factory=lambda: self._backend.create_gauge(
                name,
                description,
                labels,
            )
        )

    def histogram(
        self,
        name: str,
        description: str = "",
        labels: tuple[str, ...] = ()
    ) -> Histogram:
        """
        Get or create Histogram metric.

        Parameters
        ----------
        name:
            Metric name.

        description:
            Human-readable metric description.

        labels:
            Label names attached to metric.

        Returns
        -------
        Histogram
            Prometheus histogram instance.

        """
        self._validate_labels(labels)

        return self._get_or_create(
            name=name,
            expected_type=Histogram,
            factory=lambda: self._backend.create_histogram(
                name,
                description,
                labels,
            )
        )

    def get(self, name: str) -> object | None:
        """
        Get registered metric.

        This method does not create a metric.

        Parameters
        ----------
        name:
            Metric name.

        Returns
        -------
        object | None
            Registered metric instance or None if metric doesn't exist.

        """
        with self._lock:
            return self._metrics.get(name)

    def require(self, name: str) -> object:
        """
        Get registered metric.

        Unlike ``get()``, this method requires the metric to exist.

        Parameters
        ----------
        name:
            Metric name.

        Returns
        -------
        object
            Registered metric instance.

        Raises
        ------
        MetricNotFoundError
            If metric is not registered.

        """
        with self._lock:
            metric = self._metrics.get(name)

            if metric is None:
                msg = f"Metric '{name}' is not registered"
                raise MetricNotFoundError(msg)

            return metric

    def metric_type(self, name: str) -> type[object] | None:
        """
        Get registered metric type.

        Parameters
        ----------
        name:
            Metric name.

        Returns
        -------
        type[object] | None
            Metric type or None if metric is not registered.

        """
        with self._lock:
            return self._types.get(name)

    def _get_or_create(
        self,
        name: str,
        expected_type: type[MetricT],
        factory: Callable[[], MetricT],
    ) -> MetricT:
        """
        Get existing metric or create a new one.

        This method is the single synchronization point
        for metric registration.

        Guarantees:
        - only one metric instance exists;
        - concurrent creation is safe;
        - metric type cannot change.

        Returns
        -------
            MetricT
                Existing or newly created metric.

        Raises
        ------
        MetricRegistrationError
            If metric name already belongs to another type.

        """
        self._validate_name(name)

        with self._lock:
            existing = self._metrics.get(name)

            if existing is not None:
                registered_type = self._types[name]

                if registered_type is not expected_type:
                    msg = (
                        f"Metric '{name}' already registered as "
                        f"{registered_type.__name__}"
                    )
                    raise MetricRegistrationError(msg)

                return cast("MetricT", existing)

            metric = factory()
            self._metrics[name] = metric
            self._types[name] = expected_type

            return metric

    @staticmethod
    def _validate_name(name: str) -> None:
        """
        Validate metric name.

        Raises
        ------
        MetricConfigurationError
            If metric name is empty.

        """
        if not name.strip():
            msg = "Metric name cannot be empty"
            raise MetricConfigurationError(msg)

    @staticmethod
    def _validate_labels(labels: tuple[str, ...]) -> None:
        """
        Validate metric labels.

        Parameters
        ----------
        labels:
            Prometheus label names.

        Raises
        ------
        MetricConfigurationError
            If labels contain duplicates.

        """
        if len(labels) != len(set(labels)):
            msg = "Metric labels must be unique"
            raise MetricConfigurationError(msg)


__all__ = ("MetricManager",)
