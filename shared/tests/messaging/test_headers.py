from __future__ import annotations

from shared.messaging import headers


def test_header_names_are_unique() -> None:
    values = [
        value
        for name, value in vars(headers).items()
        if name.isupper()
    ]

    assert len(values) == len(set(values))


def test_trace_headers() -> None:
    assert headers.TRACE_PARENT == "traceparent"
    assert headers.TRACE_STATE == "tracestate"


def test_message_headers() -> None:
    assert headers.MESSAGE_ID == "message-id"
    assert headers.CORRELATION_ID == "correlation-id"
    assert headers.CAUSATION_ID == "causation-id"


def test_payload_headers() -> None:
    assert headers.CONTENT_TYPE == "content-type"
    assert headers.CONTENT_ENCODING == "content-encoding"
    assert headers.SCHEMA_VERSION == "schema-version"

def test_headers_are_defined() -> None:
    """
    Header constants exist.
    """

    assert headers.MESSAGE_ID == "message_id"
    assert headers.CORRELATION_ID == "correlation_id"
    assert headers.CAUSATION_ID == "causation_id"


def test_json_content_type() -> None:
    """
    JSON content type is stable.
    """

    assert (
        headers.JSON_CONTENT_TYPE
        ==
        "application/json"
    )
