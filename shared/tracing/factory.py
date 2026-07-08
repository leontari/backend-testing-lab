"""
TraceFactory — centralized trace construction logic.

This component is responsible for creating TraceContext instances
from different sources:

- Root traces (new incoming requests)
- Remote traces (propagated from other services)
- Child spans (internal execution flow)

It does NOT:

- interact with HTTP/gRPC/Kafka
- parse headers
- manage ContextVar state
"""

from __future__ import annotations

import uuid

from .constants import TRACE_FLAGS_NOT_SAMPLED
from .models import RawTraceCarrier, TraceContext


class TraceFactory:
    """Factory for creating TraceContext instances."""

    @staticmethod
    def create_root_trace() -> TraceContext:
        """
        Create a new root trace.

        Used when no incoming trace context exists.

        Returns
        -------
        TraceContext
            New root trace.

        """
        trace_id = TraceFactory._generate_trace_id()
        span_id = TraceFactory._generate_span_id()

        return TraceContext(
            version="00",
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            trace_flags=TRACE_FLAGS_NOT_SAMPLED,
            tracestate=None,
            created_at=TraceContext.now(),
        )

    @staticmethod
    def create_remote_trace(carrier: RawTraceCarrier) -> TraceContext:
        """
        Create trace from remote propagated context.

        This is used when request comes from another service.

        Parameters
        ----------
        carrier:
            Incoming transport trace context.

        Returns
        -------
        TraceContext
            Restored trace context.

        """
        return TraceContext(
            version=carrier.version,
            trace_id=carrier.trace_id,
            span_id=TraceFactory._generate_span_id(),
            parent_span_id=carrier.span_id,
            trace_flags=carrier.trace_flags,
            tracestate=carrier.tracestate,
            created_at=TraceContext.now(),
        )

    @staticmethod
    def create_child_span(current: TraceContext) -> TraceContext:
        """
        Create child span from current trace context.

        Used for internal operations (DB calls, services, tasks).

        Parameters
        ----------
        current:
            Active trace context.

        Returns
        -------
        TraceContext
            New child span.

        """
        return TraceContext(
            version=current.version,
            trace_id=current.trace_id,
            span_id=TraceFactory._generate_span_id(),
            parent_span_id=current.span_id,
            trace_flags=current.trace_flags,
            tracestate=current.tracestate,
            created_at=TraceContext.now(),
        )

    @staticmethod
    def _generate_trace_id() -> str:
        """
        Generate W3C-compliant trace_id (32 hex chars).

        Returns
        -------
        str
            Trace identifier.

        """
        return uuid.uuid4().hex + uuid.uuid4().hex[:16]

    @staticmethod
    def _generate_span_id() -> str:
        """
        Generate W3C-compliant span_id (16 hex chars).

        Returns
        -------
        str
            Span identifier.

        """
        return uuid.uuid4().hex[:16]
