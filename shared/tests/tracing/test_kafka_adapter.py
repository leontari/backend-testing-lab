from shared.tracing.transport.kafka import kafka_trace_adapter


def test_kafka_to_mapping():
    headers = [
        ("traceparent", b"00-aaa-bbb-01"),
        ("user-id", b"42"),
    ]

    result = kafka_trace_adapter.to_mapping(headers)

    assert result["traceparent"] == "00-aaa-bbb-01"
    assert result["user-id"] == "42"


def test_kafka_build_carrier():
    headers = [("x", b"1")]

    result = kafka_trace_adapter.build_carrier(
        headers,
        {"traceparent": "00-aaa-bbb-01"},
    )

    assert ("traceparent", b"00-aaa-bbb-01") in result
    assert ("x", b"1") in result
