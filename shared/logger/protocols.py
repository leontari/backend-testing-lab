"""Logger integration protocols."""

from __future__ import annotations

from typing import Protocol


class TraceProvider(Protocol):
    """
    Trace context provider.

    Logger uses this protocol to obtain
    distributed tracing metadata.

    Logger does not depend on tracing implementation.

    """

    def current_trace(self) -> dict[str, str | None]:
        """
        Return current trace metadata.

        Returns
        -------
        dict
            Trace fields.

        """
