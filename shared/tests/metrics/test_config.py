from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from shared.metrics.config import MetricsConfig


def test_metrics_config_default_values(config: MetricsConfig) -> None:
    """MetricsConfig should provide valid default configuration."""
    assert config.namespace == "application"
    assert config.histogram_buckets == (
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


def test_metrics_config_custom_values() -> None:
    """MetricsConfig should accept custom runtime configuration."""
    config = MetricsConfig(
        namespace="orders",
        histogram_buckets=(
            0.01,
            0.1,
            1.0,
        ),
    )

    assert config.namespace == "orders"
    assert config.histogram_buckets == (0.01, 0.1, 1.0)


def test_metrics_config_is_immutable(config: MetricsConfig) -> None:
    """
    MetricsConfig should be immutable because it represents
    application runtime configuration.
    """
    with pytest.raises(FrozenInstanceError):
        config.namespace = "changed"


def test_metrics_config_does_not_allow_new_attributes(
    config: MetricsConfig
) -> None:
    """MetricsConfig with slots=True should not allow dynamic attributes."""
    with pytest.raises(TypeError), pytest.raises(AttributeError):
        config.custom_value = 123


def test_metrics_config_hashable(config: MetricsConfig) -> None:
    """
    Frozen dataclass should be hashable and usable as immutable
    configuration object.
    """
    assert isinstance(hash(config), int)


def test_metrics_config_buckets_are_tuple(config: MetricsConfig) -> None:
    """
    Histogram buckets should be immutable sequence.
    """
    assert isinstance(config.histogram_buckets, tuple)
    assert all(
        isinstance(bucket, float) for bucket in config.histogram_buckets
    )


def test_metrics_config_buckets_are_sorted(config: MetricsConfig) -> None:
    """
    Histogram buckets must be ordered ascending because Prometheus
    expects increasing bucket boundaries.
    """
    assert config.histogram_buckets == tuple(sorted(config.histogram_buckets))
