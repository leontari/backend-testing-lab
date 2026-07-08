"""
Kafka trace adapter.

Kafka headers are list[tuple[str, bytes]].

Converts Kafka message headers to W3C Trace Context representation.

Kafka headers differ from HTTP/gRPC in that values are stored as bytes.
This adapter is responsible for safe encoding/decoding.

The adapter is independent of aiokafka or confluent-kafka libraries.
It operates only on primitive Python structures.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import TraceTransportAdapter

if TYPE_CHECKING:
    from collections.abc import Mapping

KafkaHeaders = list[tuple[str, bytes]]


class KafkaTraceAdapter(TraceTransportAdapter[KafkaHeaders]):
    """Kafka tracing adapter."""

    def to_mapping(
        self,
        carrier: KafkaHeaders,
    ) -> Mapping[str, str]:
        """
        Convert Kafka headers into string mapping.

        Parameters
        ----------
        carrier
            Kafka message headers.

        Returns
        -------
        Mapping[str, str]
            Decoded header mapping.

        """
        return {
            k: v.decode("utf-8")
            for k, v in carrier
            if v is not None
        }

    def build_carrier(
        self,
        carrier: KafkaHeaders,
        headers: Mapping[str, str],
    ) -> KafkaHeaders:
        """
        Build Kafka headers with injected tracing context.

        Existing headers are preserved unless overwritten by tracing keys.

        Parameters
        ----------
        carrier
            Original Kafka headers.

        headers
            W3C trace headers.

        Returns
        -------
        KafkaHeaders
            Updated Kafka headers.

        """
        merged: dict[str, bytes] = {
            k: v
            for k, v in carrier
            if v is not None
        }

        for k, v in headers.items():
            merged[k] = v.encode("utf-8")

        return list(merged.items())


kafka_trace_adapter = KafkaTraceAdapter()
