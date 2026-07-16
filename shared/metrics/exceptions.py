"""
Metrics module exceptions.

This module defines exceptions raised by the metrics subsystem.

Exceptions are intentionally backend-agnostic.
They describe errors related to the metrics API lifecycle,
not errors from a specific metrics backend.

Backend-specific exceptions (for example prometheus_client errors)
should not leak outside the metrics abstraction layer.

"""

from __future__ import annotations


class MetricsError(RuntimeError):
    """
    Base exception for all metrics-related errors.

    Applications may catch this exception when they need to handle
    metrics subsystem failures without depending on internal details.

    """


class MetricRegistrationError(MetricsError):
    """
    Raised when metric registration fails.

    Examples:
    - metric with incompatible definition already exists;
    - duplicated metric name with different type;
    - invalid metric configuration.

    """


class MetricNotFoundError(MetricsError):
    """
    Raised when requested metric does not exist.

    This exception is mainly used by explicit lookup APIs.

    Lazy metric creation normally prevents this error during normal
    operation.

    """


class MetricConfigurationError(MetricsError):
    """
    Raised when metric configuration is invalid.

    Examples:
    - empty metric name;
    - invalid labels;
    - unsupported configuration values.

    """


__all__ = (
    "MetricConfigurationError",
    "MetricNotFoundError",
    "MetricRegistrationError",
    "MetricsError",
)
