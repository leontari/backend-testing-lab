"""
Distributed trace propagation.

Implements W3C Trace Context propagation.

Responsibilities:

- extract trace information
- inject trace information

Does not:

- create spans
- store contexts
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from .constants import TRACE_VERSION
from .exceptions import InvalidTraceParentError
from .models import TraceContext

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping


class TracePropagator:
    """W3C trace context propagator."""

    def extract(self, carrier: Mapping[str, str]) -> TraceContext | None:
        """
        Extract TraceContext from carrier.

        Carrier example:
            {
                "traceparent": "...",
                "tracestate": "..."
            }
        """
        traceparent = carrier.get("traceparent")

        if traceparent is None:
            return None

        return self._parse(traceparent, carrier.get("tracestate"))

    def inject(
        self,
        context: TraceContext,
        carrier: MutableMapping[str, str],
    ) -> None:
        """Inject TraceContext into carrier."""

        carrier["traceparent"] = context.traceparent

        if context.tracestate is not None:
            carrier["tracestate"] = context.tracestate

    def _parse(self, traceparent: str, tracestate: str | None) -> TraceContext:
        """Parse W3C traceparent."""
        parts = traceparent.split("-")

        if len(parts) != 4:
            msg = "Invalid traceparent format"
            raise InvalidTraceParentError(msg)

        version, trace_id, span_id, flags = parts

        if version != TRACE_VERSION:
            msg = f"Unsupported version {version}"
            raise InvalidTraceParentError(msg)

        return TraceContext(
            version=version,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=None,
            trace_flags=flags,
            tracestate=tracestate,
            created_at=datetime.now(UTC),
            remote=True,
        )
