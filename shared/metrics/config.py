"""
Metrics configuration.

Contains runtime configuration shared by metric backends.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricsConfig:
    """
    Runtime metrics configuration.

    This configuration defines global metric policies.

    Parameters
    ----------
    namespace:
        Prometheus namespace prefix.

    histogram_buckets:
        Default latency buckets used by histogram metrics.

    """

    namespace: str = "application"
    histogram_buckets: tuple[float, ...] = (
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
    )


__all__ = ("MetricsConfig",)
