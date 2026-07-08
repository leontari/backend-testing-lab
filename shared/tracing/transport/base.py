"""
Base transport adapter for distributed tracing.

Transport adapters convert transport-specific header collections
into generic mappings understood by TracePropagator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from ..propagator import trace_propagator

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..models import RawTraceCarrier

CarrierT = TypeVar("CarrierT")


class TraceTransportAdapter(ABC, Generic[CarrierT]):
    """
    Base transport adapter.

    Concrete adapters implement conversion between transport-native
    header containers and plain string mappings.
    """

    @abstractmethod
    def to_mapping(
        self,
        carrier: object,
    ) -> Mapping[str, str]:
        """
        Convert transport headers into a string mapping.

        Parameters
        ----------
        carrier
            Native transport headers.

        Returns
        -------
        Mapping[str, str]
            Normalized headers.

        """

    @abstractmethod
    def build_carrier(
        self,
        carrier: object,
        headers: Mapping[str, str],
    ) -> object:
        """
        Write normalized headers back into the transport container.

        Parameters
        ----------
        carrier
            Native transport headers.

        headers
            Normalized tracing headers.

        Returns
        -------
        object
            Updated transport container.

        """

    def extract(
        self,
        carrier: CarrierT,
    ) -> RawTraceCarrier | None:
        """
        Extract transport trace.

        Parameters
        ----------
        carrier
            Native transport headers.

        Returns
        -------
        RawTraceCarrier | None

        """
        return trace_propagator.extract(self.to_mapping(carrier))

    def inject(
        self,
        trace: RawTraceCarrier,
        carrier: object,
    ) -> object:
        """
        Inject transport trace.

        Parameters
        ----------
        trace
            Transport trace.

        carrier
            Native transport container.

        Returns
        -------
        object
            Updated transport container.

        """
        headers: dict[str, str] = {}

        trace_propagator.inject(
            trace,
            headers,
        )

        return self.build_carrier(
            carrier,
            headers,
        )
