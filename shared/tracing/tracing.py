"""
Public tracing API.

Application should only import this object.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from shared.tracing.manager import TraceManager
from shared.tracing.propagator import TracePropagator
from shared.tracing.transport import TransportRegistry

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from shared.tracing.models import TraceContext


@dataclass(slots=True, frozen=True)
class Tracing:
    """
    Unified tracing facade.

    This is the only public tracing object.
    """

    _manager: TraceManager = field(default_factory=TraceManager)
    _propagator: TracePropagator = field(default_factory=TracePropagator)
    _transport: TransportRegistry = field(default_factory=TransportRegistry)

    #############
    # Runtime API
    #############

    def current(self) -> TraceContext | None:
        """Return current trace."""
        return self._manager.store.current()

    @asynccontextmanager
    async def span(
        self,
        source: TraceContext | None = None,
    ) -> AsyncIterator[TraceContext]:
        """Create runtime span."""
        async with self._manager.span(source) as context:
            yield context

    #################
    # Propagation API
    #################

    def extract(self, carrier: Any) -> TraceContext | None:
        """
        Extract trace from transport carrier.
        """
        headers = self._transport.extract(carrier)

        return self._propagator.extract(headers)

    def inject(self, context: TraceContext | None, carrier: Any) -> Any:
        """
        Inject trace into transport carrier.
        """
        if context is None:
            return carrier

        headers: dict[str, str] = {}
        self._propagator.inject(context, headers)

        return self._transport.inject(carrier, headers)

    ###############
    # Extension API
    ###############

    def register_transport(
        self,
        carrier_type: type,
        *,
        extract,
        inject,
    ) -> None:
        """
        Register custom transport.
        """
        self._transport.register(
            carrier_type,
            extract=extract,
            inject=inject,
        )


__all__ = ("Tracing",)
