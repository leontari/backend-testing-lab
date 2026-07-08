"""
Distributed tracing domain models.

This module contains immutable runtime and transport models used by the
distributed tracing subsystem.

The tracing implementation follows the W3C Trace Context specification:

https://www.w3.org/TR/trace-context/

Two independent models are defined:

* RawTraceCarrier
    Transport-level representation exchanged between services.

* TraceContext
    Runtime representation stored inside ContextVar.

The transport model intentionally knows nothing about runtime state,
while the runtime model knows nothing about transport protocols.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime

from .constants import (
    SPAN_ID_LENGTH,
    TRACE_FLAGS_NOT_SAMPLED,
    TRACE_FLAGS_SAMPLED,
    TRACE_ID_LENGTH,
    TRACEPARENT_HEADER,
    TRACESTATE_HEADER,
)
from .exceptions import InvalidTraceParentError

_HEX_RE = re.compile(r"^[0-9a-f]+$")


@dataclass(slots=True, frozen=True)
class RawTraceCarrier:
    """
    W3C Trace Context transport representation.

    RawTraceCarrier is an immutable value object describing trace
    information transferred between services.

    It is completely transport-neutral and may be used with:

    - HTTP
    - gRPC
    - Kafka
    - NATS
    - AMQP
    - RabbitMQ
    - any custom transport

    The object intentionally contains no runtime state and is never
    stored inside ContextVar.

    Parameters
    ----------
    version
        W3C Trace Context version.

    trace_id
        Distributed trace identifier.

    span_id
        Span identifier of the sender.

    trace_flags
        W3C trace flags.

    tracestate
        Optional vendor-specific tracing information.

    """

    version: str
    trace_id: str
    span_id: str
    trace_flags: str
    tracestate: str | None = None

    def __post_init__(self) -> None:
        """Validate the carrier."""
        self._validate_version()
        self._validate_trace_id()
        self._validate_span_id()
        self._validate_trace_flags()

    def _validate_version(self) -> None:
        """Validate trace version."""
        if len(self.version) != 2:
            msg = ("Trace version must contain exactly "
                   "two hexadecimal characters.")
            raise InvalidTraceParentError(msg)

        if not _HEX_RE.fullmatch(self.version):
            msg = "Trace version must be hexadecimal."
            raise InvalidTraceParentError(msg)

    def _validate_trace_id(self) -> None:
        """Validate trace identifier."""
        if len(self.trace_id) != TRACE_ID_LENGTH:
            msg = (
                f"Invalid trace_id length "
                f"({len(self.trace_id)}). "
                f"Expected {TRACE_ID_LENGTH}."
            )
            raise InvalidTraceParentError(msg)

        if not _HEX_RE.fullmatch(self.trace_id):
            msg = "trace_id must contain hexadecimal characters only."
            raise InvalidTraceParentError(msg)

        if int(self.trace_id, 16) == 0:
            msg = "trace_id cannot be all zeros."
            raise InvalidTraceParentError(msg)

    def _validate_span_id(self) -> None:
        """Validate span identifier."""
        if len(self.span_id) != SPAN_ID_LENGTH:
            msg = (
                f"Invalid span_id length "
                f"({len(self.span_id)}). "
                f"Expected {SPAN_ID_LENGTH}."
            )
            raise InvalidTraceParentError(msg)

        if not _HEX_RE.fullmatch(self.span_id):
            msg = "span_id must contain hexadecimal characters only."
            raise InvalidTraceParentError(msg)

        if int(self.span_id, 16) == 0:
            msg = "span_id cannot be all zeros."
            raise InvalidTraceParentError(msg)

    def _validate_trace_flags(self) -> None:
        """Validate trace flags."""
        if self.trace_flags not in {
            TRACE_FLAGS_SAMPLED,
            TRACE_FLAGS_NOT_SAMPLED,
        }:
            msg = "Unsupported trace_flags value."
            raise InvalidTraceParentError(msg)

    @property
    def traceparent(self) -> str:
        """
        Serialized W3C ``traceparent`` header.

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

    @property
    def headers(self) -> dict[str, str]:
        """
        Transport headers.

        Returns
        -------
        dict[str, str]
            Dictionary containing W3C trace headers.

        """
        headers = {TRACEPARENT_HEADER: self.traceparent}

        if self.tracestate is not None:
            headers[TRACESTATE_HEADER] = self.tracestate

        return headers

    @classmethod
    def from_traceparent(
        cls,
        traceparent: str,
        tracestate: str | None = None,
    ) -> RawTraceCarrier:
        """
        Parse a W3C ``traceparent`` header.

        Parameters
        ----------
        traceparent
            Serialized W3C traceparent header.

        tracestate
            Optional W3C tracestate header.

        Returns
        -------
        RawTraceCarrier
            Parsed transport trace context.

        Raises
        ------
        InvalidTraceParentError
            If the header is malformed.

        """
        parts = traceparent.split("-")

        if len(parts) != 4:
            msg = f"Malformed traceparent header: {traceparent!r}"
            raise InvalidTraceParentError(msg)

        version, trace_id, span_id, trace_flags = parts

        return cls(
            version=version,
            trace_id=trace_id,
            span_id=span_id,
            trace_flags=trace_flags,
            tracestate=tracestate,
        )

    def __str__(self) -> str:
        """
        Return serialized traceparent.

        Returns
        -------
        str
            W3C traceparent header.

        """
        return self.traceparent


@dataclass(slots=True, frozen=True)
class TraceContext:
    """
    Runtime distributed trace context.

    TraceContext represents the tracing state of the current execution
    flow inside a single process.

    Unlike RawTraceCarrier, this object is never transmitted over the
    network. It exists only during request processing and is stored in
    ContextVar by TraceContextStore.

    The context represents the currently executing span.

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

    Notes
    -----
    A TraceContext always belongs to exactly one execution context
    (HTTP request, gRPC request, Kafka message handler, background task,
    etc.).

    Child spans are created by TraceFactory.

    """

    version: str
    trace_id: str
    span_id: str
    parent_span_id: str | None
    trace_flags: str
    tracestate: str | None
    created_at: datetime

    @staticmethod
    def now() -> datetime:
        """
        Return current UTC timestamp.

        Returns
        -------
        datetime
            Current UTC timestamp.

        """
        return datetime.now(UTC)

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
    def carrier(self) -> RawTraceCarrier:
        """
        Convert runtime context into transport representation.

        Returns
        -------
        RawTraceCarrier
            Transport-level trace carrier.

        Notes
        -----
        The current span becomes the sender span in the outgoing
        transport headers.

        """
        return RawTraceCarrier(
            version=self.version,
            trace_id=self.trace_id,
            span_id=self.span_id,
            trace_flags=self.trace_flags,
            tracestate=self.tracestate,
        )

    def __str__(self) -> str:
        """
        Return human-readable representation.

        Returns
        -------
        str
            Short textual representation of the trace context.

        """
        return (
            "TraceContext("
            f"trace_id={self.trace_id}, "
            f"span_id={self.span_id}, "
            f"parent_span_id={self.parent_span_id})"
        )
