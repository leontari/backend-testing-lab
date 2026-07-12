from tracing.transport import (
    TransportRegistry,
)



class FakeHeaders(dict):
    pass



def test_mapping_transport():

    registry = TransportRegistry()


    registry.register(
        FakeHeaders,

        extract=lambda x: x,

        inject=lambda x,h:
            x.update(h),
    )


    headers = FakeHeaders(
        traceparent="abc"
    )


    result = registry.extract(
        headers
    )


    assert result["traceparent"] == "abc"



def test_inject_transport():

    registry = TransportRegistry()


    registry.register(
        FakeHeaders,

        extract=lambda x: x,

        inject=lambda x,h:
            x.update(h),
    )


    headers = FakeHeaders()


    registry.inject(
        headers,
        {
            "traceparent":"abc"
        }
    )


    assert headers[
        "traceparent"
    ] == "abc"
