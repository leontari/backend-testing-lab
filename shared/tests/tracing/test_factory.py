from shared.tracing.factory import TraceFactory
from shared.tracing.models import TraceContext


def test_create_root_context():
    factory = TraceFactory()
    context = factory.create()

    assert context.trace_id
    assert context.span_id
    assert context.parent_span_id is None


def test_create_child_context():
    factory = TraceFactory()
    parent = factory.create()
    child = factory.create(source=parent)

    assert child.trace_id == parent.trace_id
    assert child.parent_span_id == parent.span_id
    assert child.span_id != parent.span_id
