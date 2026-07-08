"""
Runtime TraceContext manager.

Responsible for lifecycle management of TraceContext.

The manager does not know anything about HTTP,
Kafka or gRPC transports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from .exceptions import TraceContextMissingError
from .propagator import TracePropagator

if TYPE_CHECKING:
    from contextvars import Token

    from .factory import TraceFactory
    from .models import RawTraceCarrier, TraceContext
    from .store import TraceContextStore


class TraceManager:
    """Runtime TraceContext lifecycle manager."""

    def __init__(
        self,
        *,
        factory: TraceFactory,
        propagator: TracePropagator,
        store: TraceContextStore,
    ) -> None:
        """
        Initialize TraceManager.

        Parameters
        ----------
        store:
            Runtime TraceContext storage.

        factory:
            TraceContext factory.

        """
        self._factory = factory
        self._propagator = propagator
        self._store = store

    def from_headers(
        self,
        headers: Mapping[str, str]
    ) -> RawTraceCarrier | None:
        trace_context = self._store.get_current_trace()

        if not trace_context:
            return

        carrier = trace_context.carrier
        headers.update(self._propagator.inject(carrier=carrier))

    def get_current_trace(
        self,
    ) -> TraceContext:
        """
        Return current TraceContext.

        Returns
        -------
        TraceContext
            Active trace.

        Raises
        ------
        TraceContextMissingError
            If no trace is installed.

        """
        trace = self._store.get_current_trace()

        if trace is None:
            msg = "No active TraceContext."
            raise TraceContextMissingError(msg)

        return trace

    def install_trace(
        self,
        trace: TraceContext,
    ) -> Token[TraceContext | None]:
        """
        Install TraceContext.

        Parameters
        ----------
        trace:
            Runtime trace.

        Returns
        -------
        Token
            Context rollback token.

        """
        return self._store.set_current_trace(trace)

    def restore_trace(
        self,
        token: Token[TraceContext | None],
    ) -> None:
        """
        Restore previous TraceContext.

        Parameters
        ----------
        token:
            Context rollback token.

        """
        self._store.reset_current_trace(token)

    def create_root_trace(
        self,
    ) -> TraceContext:
        """
        Create root TraceContext.

        Returns
        -------
        TraceContext
            Newly created root trace.

        """
        return self._factory.create_root_trace()

    def create_child_trace(
        self,
        parent: TraceContext,
    ) -> TraceContext:
        """
        Create child TraceContext.

        Parameters
        ----------
        parent:
            Parent trace.

        Returns
        -------
        TraceContext
            Child trace.

        """
        return self._factory.create_child_span(parent)

    def create_remote_trace(
        self,
        carrier: RawTraceCarrier,
    ) -> TraceContext:
        """
        Create local TraceContext from remote carrier.

        Parameters
        ----------
        carrier:
            Incoming propagated context.

        Returns
        -------
        TraceContext
            Local runtime TraceContext.

        """
        return self._factory.create_remote_trace(carrier)
