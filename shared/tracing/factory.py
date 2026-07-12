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

import secrets
from datetime import UTC, datetime

from shared.tracing.constants import (
    TRACE_FLAGS_SAMPLED,
    TRACE_VERSION,
)
from shared.tracing.models import TraceContext
from shared.tracing.validation import validate_trace_context


class TraceFactory:
    """Factory for creating TraceContext instances."""

    def create(self, source: TraceContext | None = None) -> TraceContext:
        """
        Create a new trace context.

        Parameters
        ----------
        source:
            Existing trace context used as a source for creating a new span.

            None:
                create a new root trace

            TraceContext:
                create a child span

        Returns
        -------
        TraceContext
            New runtime trace context.

        """
        if source is None:
            return self._create_root_trace()

        return self._create_child_trace(source)

    def _create_root_trace(self) -> TraceContext:
        """
        Create a new root trace context.

        Example:
            HTTP request without traceparent header.

        Returns:
            TraceContext:
                a new root context that starts a new distributed trace.

        """
        return self._create(
            version=TRACE_VERSION,
            trace_id=self._new_trace_id(),
            parent_span_id=None,
            span_id=self._new_span_id(),
            trace_flags=TRACE_FLAGS_SAMPLED,
            tracestate=None,
            remote=False,
        )

    def _create_child_trace(self, source: TraceContext) -> TraceContext:
        """
        Create a child trace for incoming trace.

        Keeps the same trace_id and creates a new span_id.
        spand_id of source object becomes parent_span_id.

        Source can be:
        - local trace context
        - remote trace context
        - workflow trace context

        Example:
            HTTP request trace -> payment.process trace

        Returns:
        TraceContext
            New trace created from incoming trace.

        """
        return self._create(
            version=source.version,
            trace_id=source.trace_id,
            span_id=self._new_span_id(),
            parent_span_id=source.span_id,
            trace_flags=source.trace_flags,
            tracestate=source.tracestate,
            remote=False,
        )

    @staticmethod
    def _create(
        *,
        version: str,
        trace_id: str,
        span_id: str,
        parent_span_id: str | None,
        trace_flags: str,
        tracestate: str | None,
        remote: bool,
        created_at: datetime | None = None,
    ) -> TraceContext:
        """
        Single TraceContext construction point.

        All contexts must pass through this method.

        Returns:
            New TraceContext object.

        """
        validate_trace_context(
            version=version,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            trace_flags=trace_flags,
        )

        return TraceContext(
            version=version,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            trace_flags=trace_flags,
            tracestate=tracestate,
            created_at=created_at or datetime.now(UTC),
            remote=remote,
        )

    @staticmethod
    def _new_trace_id() -> str:
        """
        Generate 128-bit trace id.

        Returns:
            New trace identifier.

        """
        return secrets.token_hex(16)

    @staticmethod
    def _new_span_id() -> str:
        """
        Generate 64-bit span id.

        Returns:
            New span identifier

        """
        return secrets.token_hex(8)

    # @staticmethod
    # def _generate_trace_id() -> str:
    #     """
    #     Generate W3C-compliant trace_id (32 hex chars).
    #
    #     Returns
    #     -------
    #     str
    #         Trace identifier.
    #
    #     """
    #     return uuid.uuid4().hex + uuid.uuid4().hex[:16]
    #
    # @staticmethod
    # def _generate_span_id() -> str:
    #     """
    #     Generate W3C-compliant span_id (16 hex chars).
    #
    #     Returns
    #     -------
    #     str
    #         Span identifier.
    #
    #     """
    #     return uuid.uuid4().hex[:16]


__all__ = ("TraceFactory",)
