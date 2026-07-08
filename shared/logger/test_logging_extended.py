from __future__ import annotations

import logging

from shared.logger.logger import TraceLoggingFilter
from shared.tracing.factory import TraceFactory
from shared.tracing.manager import TraceManager


def test_logging_contains_trace_fields():
    manager = TraceManager()
    trace = TraceFactory.create_root_trace()

    manager.install_trace(trace)

    logger = logging.getLogger("trace-test")
    logger.addFilter(TraceLoggingFilter(manager))

    record = logger.makeRecord(
        name="trace-test",
        level=logging.INFO,
        fn="f",
        lno=10,
        msg="hello",
        args=(),
        exc_info=None,
    )

    assert hasattr(record, "trace_id")
    assert hasattr(record, "span_id")
    assert hasattr(record, "trace_id")
