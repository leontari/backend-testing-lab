import pytest

from shared.tracing.tracing import Tracing


@pytest.mark.asyncio
async def test_http_kafka_grpc_flow():
    tracing = Tracing()

    # HTTP
    async with tracing.span() as http_span:
        headers = {}
        tracing.inject(http_span, headers)

        # Kafka
        kafka_context = tracing.extract(headers)
        async with tracing.span(kafka_context) as kafka_span:

            # gRPC
            metadata = {}
            tracing.inject(kafka_span, metadata)
            grpc_context = tracing.extract(metadata)
            async with tracing.span(grpc_context) as grpc_span:

                assert grpc_span.trace_id == http_span.trace_id
                assert grpc_span.parent_span_id == kafka_span.span_id
