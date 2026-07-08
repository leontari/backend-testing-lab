"""
W3C Trace Context propagator.

Responsible only for copying tracing information
between transport headers and RawTraceCarrier.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import (
    TRACEPARENT_HEADER,
    TRACESTATE_HEADER,
)
from .models import RawTraceCarrier

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping


class TracePropagator:
    """Transport-independent propagator."""

    def extract(
        self,
        carrier: Mapping[str, str],
    ) -> RawTraceCarrier | None:
        """
        Extract tracing information from transport headers.

        Parameters
        ----------
        carrier:
            Transport headers.

        Returns
        -------
        RawTraceCarrier | None
            Parsed carrier or None if tracing headers
            are not present.

        """
        traceparent = carrier.get(TRACEPARENT_HEADER)

        if traceparent is None:
            return None

        return RawTraceCarrier.from_traceparent(
            traceparent=traceparent,
            tracestate=carrier.get(TRACESTATE_HEADER),
        )

    def inject(
        self,
        trace: RawTraceCarrier,
        carrier: MutableMapping[str, str],
    ) -> None:
        """
        Inject tracing information into transport headers.

        Parameters
        ----------
        trace:
            Trace carrier.

        carrier:
            Mutable transport headers.

        """
        carrier[TRACEPARENT_HEADER] = trace.traceparent

        if trace.tracestate is not None:
            carrier[TRACESTATE_HEADER] = trace.tracestate
