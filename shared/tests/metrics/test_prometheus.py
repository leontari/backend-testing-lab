from prometheus_client import CollectorRegistry

from shared.metrics.config import MetricsConfig
from shared.metrics.prometheus import PrometheusBackend


def create_backend() -> PrometheusBackend:
    """Create isolated backend for tests."""

    return PrometheusBackend(
        config=MetricsConfig(
            namespace="test",
            histogram_buckets=(0.1, 0.5, 1.0),
        ),
        registry=CollectorRegistry(),
    )


def test_create_counter() -> None:
    """
    Backend should create working counter.
    """

    backend = create_backend()

    counter = backend.create_counter(
        name="requests_total",
        description="Requests",
    )
    counter.inc()
    samples = list(backend.registry.collect())

    assert len(samples) == 1
    assert samples[0].name == "test_requests"


def test_create_counter_with_labels() -> None:
    """
    Counter should support labels.
    """
    backend = create_backend()

    counter = backend.create_counter(
        name="requests_total",
        description="Requests",
        labels=(
            "method",
        ),
    )

    counter.labels(method="GET").inc()
    samples = list(backend.registry.collect())

    assert samples


def test_create_gauge() -> None:
    """
    Backend should create gauge.
    """

    backend = create_backend()

    gauge = backend.create_gauge(
        name="connections",
        description="Connections",
    )

    gauge.set(10)
    samples = list(backend.registry.collect())

    assert samples


def test_create_histogram() -> None:
    """
    Backend should create histogram.
    """
    backend = create_backend()
    histogram = backend.create_histogram(
        name="request_duration",
        description="Duration",
    )
    histogram.observe(0.25)
    samples = list(backend.registry.collect())

    assert samples


def test_namespace_is_applied() -> None:
    """
    Backend should apply configured namespace.
    """
    backend = create_backend()
    counter = backend.create_counter(
        name="created_total",
        description="Created",
    )
    counter.inc()
    metric = list(backend.registry.collect())[0]

    assert metric.name == "test_created"


def test_histogram_buckets_are_applied() -> None:
    """
    Backend should configure histogram buckets.
    """
    backend = create_backend()
    histogram = backend.create_histogram(
        name="duration",
        description="Duration",
    )
    histogram.observe(0.3)
    samples = list(backend.registry.collect())

    assert samples
