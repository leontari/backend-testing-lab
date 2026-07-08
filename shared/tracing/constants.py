"""
W3C Trace Context constants.

Defines protocol-level constants used for propagation
of distributed tracing across HTTP, gRPC and Kafka.

Specification:
https://www.w3.org/TR/trace-context/
"""

# HTTP transport header name for trace context.
TRACEPARENT_HEADER: str = "traceparent"

# Optional vendor-specific tracing state.
TRACESTATE_HEADER: str = "tracestate"

# Current supported W3C trace context version.
TRACE_VERSION: str = "00"

TRACE_FLAGS_SAMPLED: str = "01"
TRACE_FLAGS_NOT_SAMPLED: str = "00"

TRACE_ID_LENGTH: int = 32
SPAN_ID_LENGTH: int = 16
