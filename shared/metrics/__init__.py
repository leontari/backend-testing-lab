"""
Metrics package.

Public API for application metrics.

The package exposes only high-level runtime interfaces.

Example:
-------
    from metrics import Metrics

    metrics = Metrics()
    metrics.increment("orders.created.total")

"""

from __future__ import annotations

from shared.metrics.metrics import Metrics

from .exceptions import (
    MetricConfigurationError,
    MetricNotFoundError,
    MetricRegistrationError,
    MetricsError,
)

__version__ = "0.1.0"

__all__ = (
    "MetricConfigurationError",
    "MetricNotFoundError",
    "MetricRegistrationError",
    "Metrics",
    "MetricsError",
    "__version__",
)
