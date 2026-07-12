"""
Distributed tracing module.

Provides W3C-compatible trace context propagation
for HTTP, gRPC and Kafka transports.

"""

from __future__ import annotations

from shared.tracing.fastapi import TraceMiddleware
from shared.tracing.models import TraceContext
from shared.tracing.tracing import Tracing

__version__ = "1.0.0"

__all__ = (
    "TraceContext",
    "TraceMiddleware",
    "Tracing",
    "__version__",
)
