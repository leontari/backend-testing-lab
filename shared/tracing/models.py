"""
Distributed tracing domain models.

This module contains immutable runtime trace context models used by the
distributed tracing subsystem.

The tracing implementation follows the W3C Trace Context specification:

https://www.w3.org/TR/trace-context/

Runtime representation stored inside ContextVar.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from shared.tracing.constants import (
    TRACE_FLAGS_NOT_SAMPLED,
    TRACE_FLAGS_SAMPLED,
    TRACEPARENT_HEADER,
    TRACESTATE_HEADER,
)

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(slots=True, frozen=True)
class TraceContext:
    """
    Runtime distributed tracing context.

    TraceContext is an immutable value object describing trace
    information transferred between services.

    It is completely transport-neutral and may be used with:
    - HTTP
    - gRPC
    - Kafka
    - NATS
    - AMQP
    - RabbitMQ
    - any custom transport

    Parameters
    ----------
    version
        W3C Trace Context version.

    trace_id
        Distributed trace identifier shared by every service
        participating in the request.

    span_id
        Identifier of the currently executing span.

    parent_span_id
        Identifier of the parent span.
        For root spans this value is None.

    trace_flags
        W3C trace flags.

    tracestate
        Optional vendor-specific trace state.

    created_at
        UTC timestamp when this runtime span was created.

    remote:
        a flag that marks whether trace_id came from network


    Notes
    -----
    A TraceContext always belongs to exactly one execution context
    (HTTP request, gRPC request, Kafka message handler, background task,
    etc.).

    TraceContext is created by TraceFactory.

    """

    version: str
    trace_id: str
    span_id: str
    parent_span_id: str | None
    trace_flags: str
    tracestate: str | None
    created_at: datetime
    remote: bool

    @property
    def is_root(self) -> bool:
        """
        Check whether this is a root span.

        Returns
        -------
        bool
            True if the span has no parent.

        """
        return self.parent_span_id is None

    @property
    def is_sampled(self) -> bool:
        """
        Check whether tracing is sampled.

        Returns
        -------
        bool
            True if trace sampling is enabled.

        """
        return self.trace_flags == TRACE_FLAGS_SAMPLED

    @property
    def is_not_sampled(self) -> bool:
        """
        Check whether tracing is disabled.

        Returns
        -------
        bool
            True if trace sampling is disabled.

        """
        return self.trace_flags == TRACE_FLAGS_NOT_SAMPLED

    @property
    def traceparent(self) -> str:
        """
        Serializes W3C traceparent header.

        Returns
        -------
        str
            Serialized traceparent header.

        """
        return (
            f"{self.version}-"
            f"{self.trace_id}-"
            f"{self.span_id}-"
            f"{self.trace_flags}"
        )

    def headers(self) -> dict[str, str]:
        """
        Build transport headers.

        Returns
        -------
        dict[str, str]
            Dictionary containing W3C trace headers.

        """
        headers = {TRACEPARENT_HEADER: self.traceparent}

        if self.tracestate is not None:
            headers[TRACESTATE_HEADER] = self.tracestate

        return headers


__all__ = ("TraceContext",)
