from shared.tracing.transport.http import http_trace_adapter


def test_http_extract_to_mapping():
    headers = {
        "traceparent": "00-" + "a" * 32 + "-" + "b" * 16 + "-01"
    }

    carrier = http_trace_adapter.to_mapping(headers)

    assert carrier["traceparent"] == headers["traceparent"]


def test_http_inject_headers():
    base = {"x-custom": "1"}

    result = http_trace_adapter.build_carrier(
        base,
        {"traceparent": "00-aaa-bbb-01"},
    )

    assert "traceparent" in result
    assert result["x-custom"] == "1"
