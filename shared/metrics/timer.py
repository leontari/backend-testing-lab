"""
Metric timer utilities.

This module provides synchronous and asynchronous context managers
for measuring execution duration using Prometheus Histogram.

The timer does not calculate duration manually.
The actual measurement is delegated to prometheus_client.

Example:
-------
Synchronous:
    with metrics.timer("database.query.seconds"):
        repository.load()

Asynchronous:
    async with metrics.timer("grpc.request.seconds"):
        await client.call()

"""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from types import TracebackType


class TimerContext(Protocol):
    """
    Timer context protocol.

    Compatible with prometheus_client Histogram.time()

    """

    def __enter__(self) -> None:
        """Start timer measurement."""

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """
        Stop timer measurement.

        Returns
        -------
        bool | None
            Context manager exception handling result.

        """


class HistogramProtocol(Protocol):
    """
    Minimal Histogram interface.

    Only functionality required by MetricTimer.
    """

    def time(self) -> TimerContext:
        """
        Create a timing context manager.

        Returns
        -------
        TimerContext
            Timer context manager.

        """


class MetricTimerError(RuntimeError):
    """Raised when MetricTimer lifecycle is violated."""


@dataclass(slots=True)
class MetricTimer(AbstractContextManager):
    """
    Unified sync/async metric timer.

    Wraps Prometheus Histogram.time() context manager.

    Supports:
        with metrics.timer(...):
            ...

        async with metrics.timer(...):
            ...

    Lifecycle:
        CREATED -> ENTERED -> CLOSED

    Re-entering the same instance is forbidden. A new timer should be created.

    """

    _histogram: HistogramProtocol
    _context: TimerContext | None = field(init=False, default=None)
    _entered: bool = field(init=False, default=False)
    _closed: bool = field(init=False, default=False)

    def __enter__(self) -> None:
        """Enter synchronous context."""
        self._start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit synchronous context."""
        return self._stop(
            exc_type,
            exc_value,
            traceback,
        )

    async def __aenter__(self) -> None:
        """
        Enter asynchronous context.

        Prometheus timing itself is synchronous,
        but the surrounding operation may be async.
        """
        self._start()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit asynchronous context."""
        return self._stop(
            exc_type,
            exc_value,
            traceback,
        )

    def _start(self) -> None:
        """
        Start timer.

        Protects against:
        - double enter;
        - concurrent reuse.

        Raises
        ------
        MetricTimerError
            If timer is reused.

        """
        if self._entered:
            msg = "MetricTimer cannot be entered twice"
            raise MetricTimerError(msg)

        if self._closed:
            msg = "MetricTimer is already closed"
            raise MetricTimerError(msg)

        self._context = self._histogram.time()
        # PLC2801 is intentionally ignored.
        # This adapter manually controls the lifecycle of an external
        # context manager returned by Prometheus Histogram.time().
        self._context.__enter__()  # noqa: PLC2801
        self._entered = True

    def _stop(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """
        Stop timer.

        Raises
        ------
        MetricTimerError
            If timer was not started or already stopped.

        """
        if not self._entered:
            msg = "MetricTimer was not started"
            raise MetricTimerError(msg)

        if self._closed:
            msg = "MetricTimer already stopped"
            raise MetricTimerError(msg)

        self._closed = True

        if self._context is not None:
            self._context.__exit__(exc_type, exc_value, traceback)


__all__ = ("MetricTimer",)
