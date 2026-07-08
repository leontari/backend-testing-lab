"""
Transport adapters for distributed tracing.

Transport adapters provide integration between transport-specific
header containers and the generic W3C Trace Context propagator.

Available adapters
------------------

HTTPTraceAdapter
    HTTP headers.

GrpcTraceAdapter
    gRPC metadata.

KafkaTraceAdapter
    Kafka message headers.
"""

from .base import TraceTransportAdapter
from .grpc import GrpcTraceAdapter
from .http import HTTPTraceAdapter
from .kafka import KafkaTraceAdapter

__all__ = (
    "GrpcTraceAdapter",
    "HTTPTraceAdapter",
    "KafkaTraceAdapter",
    "TraceTransportAdapter",
)
