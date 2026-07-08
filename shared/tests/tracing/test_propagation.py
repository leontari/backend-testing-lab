from shared.tracing.models import RawTraceCarrier


def test_traceparent_roundtrip():
    carrier = RawTraceCarrier(
        version="00",
        trace_id="a" * 32,
        span_id="b" * 16,
        trace_flags="01",
    )

    traceparent = carrier.traceparent
    parsed = RawTraceCarrier.from_traceparent(traceparent)

    assert parsed.trace_id == carrier.trace_id
    assert parsed.span_id == carrier.span_id
    assert parsed.trace_flags == carrier.trace_flags
