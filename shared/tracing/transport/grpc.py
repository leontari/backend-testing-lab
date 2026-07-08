"""
gRPC trace adapter.

Works with metadata: Sequence[tuple[str, str]].

Converts gRPC metadata to and from the generic W3C Trace Context
representation.

The adapter is independent of grpc.aio and grpc.ServerContext.
It operates only on standard metadata collections.

Supported containers
--------------------

Incoming metadata:

    Sequence[tuple[str, str]]

Outgoing metadata:

    tuple[tuple[str, str], ...]

The adapter does not depend on grpc itself and therefore can be
unit-tested without starting a gRPC server.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .base import TraceTransportAdapter

GrpcMetadata = Sequence[tuple[str, str]]
GrpcMutableMetadata = tuple[tuple[str, str], ...]


class GrpcTraceAdapter(
    TraceTransportAdapter[GrpcMetadata],
):
    """gRPC Trace Context adapter."""

    def to_mapping(
        self,
        carrier: GrpcMetadata,
    ) -> Mapping[str, str]:
        """
        Convert gRPC metadata into a normalized mapping.

        Parameters
        ----------
        carrier
            Incoming gRPC metadata.

        Returns
        -------
        Mapping[str, str]
            Normalized string mapping.

        """
        return dict(carrier)

    def build_carrier(
        self,
        carrier: GrpcMetadata,
        headers: Mapping[str, str],
    ) -> GrpcMutableMetadata:
        """
        Build outgoing gRPC metadata.

        Existing metadata entries are preserved.
        Trace headers overwrite previous values if present.

        Parameters
        ----------
        carrier
            Existing metadata.

        headers
            W3C Trace Context headers.

        Returns
        -------
        tuple[tuple[str, str], ...]
            Metadata ready to be passed to a gRPC client.

        """
        merged = dict(carrier)
        merged.update(headers)

        return tuple(merged.items())


grpc_trace_adapter = GrpcTraceAdapter()
