from shared.tracing.transport.grpc import grpc_trace_adapter


def test_grpc_to_mapping():
    metadata = (
        ("traceparent", "00-aaa-bbb-01"),
        ("user-id", "123"),
    )

    result = grpc_trace_adapter.to_mapping(metadata)

    assert result["traceparent"] == "00-aaa-bbb-01"
    assert result["user-id"] == "123"


def test_grpc_build_carrier():
    metadata = (("x", "1"),)

    result = grpc_trace_adapter.build_carrier(
        metadata,
        {"traceparent": "00-aaa-bbb-01"},
    )

    assert ("traceparent", "00-aaa-bbb-01") in result
    assert ("x", "1") in result
