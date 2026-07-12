"""
Transport normalization layer.

Responsible only for converting
transport-specific containers into
normalized tracing headers.

Does not know anything about:
    - TraceContext
    - spans
    - ContextVar
    - W3C parsing
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
)
from typing import Any

ExtractHandler = Callable[[Any], Mapping[str, str]]
InjectHandler = Callable[[Any, Mapping[str, str]], Any]


class TransportRegistry:
    """Registry for transport converters."""

    def __init__(self) -> None:
        self._extractors: dict[type[Any], ExtractHandler] = {}
        self._injectors: dict[type[Any], InjectHandler] = {}

    def register(
        self,
        carrier_type: type[Any],
        *,
        extract: ExtractHandler,
        inject: InjectHandler,
    ) -> None:
        """Register transport type."""
        self._extractors[carrier_type] = extract
        self._injectors[carrier_type] = inject

    def extract(self, carrier: Any) -> Mapping[str, str]:
        """Normalize transport carrier."""
        handler = self._find(
            type(carrier),
            self._extractors,
        )

        return handler(carrier)

    def inject(
        self,
        carrier: Any,
        headers: Mapping[str, str],
    ) -> Any:
        """Inject normalized headers."""
        handler = self._find(type(carrier), self._injectors)

        return handler(carrier, headers)

    @staticmethod
    def _find(carrier_type: type[Any], registry: dict):
        for cls in carrier_type.__mro__:
            if cls in registry:
                return registry[cls]

        msg = (
            f"No tracing transport registered: "
            f"{carrier_type!r}"
        )
        raise TypeError(msg)


def create_default_transport_registry():

    registry = TransportRegistry()

    # HTTP / dict / Starlette Headers
    def extract_mapping(headers):

        return {
            key.lower(): value
            for key, value
            in headers.items()
            if key.lower()
            in {
                "traceparent",
                "tracestate",
            }
        }

    def inject_mapping(
        headers,
        values,
    ):

        headers.update(values)

        return headers

    registry.register(
        Mapping,
        extract=extract_mapping,
        inject=inject_mapping,
    )

    # Kafka
    def extract_kafka(
        headers,
    ):

        result = {}

        for key, value in headers:

            if key in {
                "traceparent",
                "tracestate",
            }:
                result[key] = value.decode(
                    "utf-8"
                )

        return result


    def inject_kafka(
        headers,
        values,
    ):

        for key, value in values.items():

            headers.append(
                (
                    key,
                    value.encode(),
                )
            )

        return headers


    registry.register(
        list,
        extract=extract_kafka,
        inject=inject_kafka,
    )

    return registry
