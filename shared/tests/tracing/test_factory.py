from shared.tracing.factory import TraceFactory


def test_create_root_trace():
    trace = TraceFactory.create_root_trace()

    assert trace.trace_id is not None
    assert trace.span_id is not None
    assert trace.parent_span_id is None


def test_create_child_span():
    root = TraceFactory.create_root_trace()
    child = TraceFactory.create_child_span(root)

    assert child.trace_id == root.trace_id
    assert child.parent_span_id == root.span_id
    assert child.span_id != root.span_id


def test_remote_trace_restoration():
    from shared.tracing.models import RawTraceCarrier
    from shared.tracing.factory import TraceFactory

    carrier = RawTraceCarrier(
        version="00",
        trace_id="a" * 32,
        span_id="b" * 16,
        trace_flags="01",
        tracestate=None,
    )

    trace = TraceFactory.create_remote_trace(carrier)

    assert trace.trace_id == carrier.trace_id
    assert trace.parent_span_id == carrier.span_id
