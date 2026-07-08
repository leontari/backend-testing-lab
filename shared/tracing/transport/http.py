"""
HTTP trace adapter.

Converts HTTP headers <-> W3C Trace Context mappings.

The adapter is intentionally independent of FastAPI,
Starlette or any other framework.

Supported containers
--------------------

- dict[str, str]
- Mapping[str, str]
- Starlette Headers
- aiohttp CIMultiDict
- any Mapping[str, str]
"""

from __future__ import annotations

from collections.abc import Mapping

from .base import TraceTransportAdapter


class HTTPTraceAdapter(
    TraceTransportAdapter[Mapping[str, str]],
):
    """Adapter for HTTP headers."""

    def to_mapping(
        self,
        carrier: Mapping[str, str],
    ) -> Mapping[str, str]:
        """
        Normalize HTTP headers.

        Parameters
        ----------
        carrier
            HTTP headers.

        Returns
        -------
        Mapping[str, str]
            Normalized headers.

        """
        return carrier

    def build_carrier(
        self,
        carrier: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> dict[str, str]:
        """
        Merge tracing headers into HTTP headers.

        Parameters
        ----------
        carrier
            Original HTTP headers.

        headers
            Tracing headers.

        Returns
        -------
        dict[str, str]
            Updated headers.

        """
        merged = dict(carrier)
        merged.update(headers)

        return merged


http_trace_adapter = HTTPTraceAdapter()
