from shared.tracing.models import TraceContext
from shared.tracing.propagator import TracePropagator


def test_extract_traceparent():
    propagator = TracePropagator()
    headers = {"traceparent": "00-1234567890abcdef-abcdef1234567890-01"}

    context = propagator.extract(headers)

    assert context.trace_id == "1234567890abcdef"


def test_inject_traceparent():
    propagator = TracePropagator()
    context = TraceContext(trace_id="trace", span_id="span")
    headers = {}

    propagator.inject(context, headers)

    assert "traceparent" in headers
