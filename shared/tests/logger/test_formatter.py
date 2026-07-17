import json
import logging

from shared.logger.context import (
    LogContext,
    reset_context,
    set_context,
)
from shared.logger.formatter import JsonFormatter


def test_json_formatter_basic() -> None:
    """Formatter should create JSON output."""
    formatter = JsonFormatter({"service": "test-service"})
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    result = formatter.format(record)
    data = json.loads(result)

    assert data["service"] == "test-service"
    assert data["level"] == "INFO"
    assert data["message"] == "hello"


def test_formatter_adds_context() -> None:
    """Formatter should include runtime context."""
    token = set_context(
        LogContext({
            "trace_id": "123",
            "request_id": "456",
        })
    )
    try:
        formatter = JsonFormatter({})
        record = logging.LogRecord(
            "test",
            logging.INFO,
            "",
            1,
            "request",
            (),
            None,
        )
        data = json.loads(formatter.format(record))

        assert data["trace_id"] == "123"
        assert data["request_id"] == "456"

    finally:
        reset_context(token)


def test_formatter_exception() -> None:
    """Formatter should serialize exceptions."""
    formatter = JsonFormatter({})
    try:
        raise ValueError("invalid")
    except ValueError:
        record = logging.LogRecord(
            "test",
            logging.ERROR,
            "",
            1,
            "failed",
            (),
            None,
        )
        record.exc_info = (
            ValueError,
            ValueError("invalid"),
            None,
        )
    data = json.loads(formatter.format(record))

    assert data["error.type"] == "ValueError"
    assert data["error.message"] == "invalid"
