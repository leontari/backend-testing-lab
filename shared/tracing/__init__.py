"""
Distributed tracing core module.

Provides W3C-compatible trace context propagation
for HTTP, gRPC and Kafka transports.

Main components:
- TraceContext
- RawTraceCarrier
- TraceFactory
- TraceContextStore
"""

from __future__ import annotations

from .factory import TraceFactory
from .models import RawTraceCarrier, TraceContext
from .store import TraceContextStore

__version__ = "0.1.1"

__all__ = (
    "RawTraceCarrier",
    "TraceContext",
    "TraceContextStore",
    "TraceFactory",
    "__version__",
)
