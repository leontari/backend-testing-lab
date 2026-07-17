"""
Application EventBus implementation.

Responsibilities:
- event publishing;
- handler resolution;
- sequential dispatch;
- lifecycle management.

EventBus does not:
- retry failed handlers;
- persist events;
- know transports;
- know Kafka/RabbitMQ/etc.

Error handling should be implemented
through middleware or transport layer.
"""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.eventbus.dispatcher import EventDispatcher
from shared.eventbus.exceptions import (
    EventDispatchError,
    HandlerNotFoundError,
    EventBusClosedError,
)
from shared.eventbus.lifecycle import EventBusState
from shared.eventbus.policy import ErrorPolicy
from shared.eventbus.registry import EventRegistry
from shared.eventbus.retry import RetryPolicy

if TYPE_CHECKING:
    from shared.messaging import Event


@dataclass(slots=True)
class EventBus:
    """
    Async application event bus.

    Provides:
    - subscription;
    - middleware pipeline;
    - retry;
    - lifecycle;
    - async dispatch.

    """

    _registry: EventRegistry = field(default_factory=EventRegistry)
    _dispatcher: EventDispatcher = field(default_factory=EventDispatcher)
    _retry: RetryPolicy = field(default_factory=RetryPolicy)
    _errors: ErrorPolicy = field(default_factory=ErrorPolicy)

    _state: EventBusState = field(
        init=False,
        default_factory=EventBusState.CREATED,
    )

    async def start(self) -> None:
        """Start EventBus."""
        self._state = EventBusState.RUNNING

    async def stop(self) -> None:
        """Shutdown EventBus."""
        self._state = EventBusState.CLOSED

    def subscribe(self, event_type: type[Event], handler: object) -> None:
        """
        Subscribe handler.

        Parameters
        ----------
        event_type:
            Event class.

        handler:
            Handler instance.

        """
        self._registry.register(event_type, handler)

    async def publish(self, event: Event) -> None:
        """
        Publish event.

        Executes all registered handlers.

        Raises
        ------
        HandlerNotFoundError
            No handlers registered.

        EventDispatchError
            Handler failed.

        """
        if self._state == EventBusState.CLOSED:
            raise EventBusClosedError

        handlers = self._registry.get(type(event))

        if not handlers:
            msg = f"No handlers for {type(event).__name__}"
            raise HandlerNotFoundError(msg)

        await asyncio.gather(
            *[self._execute(handler, event) for handler in handlers]
        )


        for handler in handlers:
            try:
                await self._execute(handler, event)
            except Exception as exc:
                msg = f"Failed processing {event}"
                raise EventDispatchError(msg) from exc

    async def _execute(self, handler: object, event: Event) -> None:
        """
        Execute handler.

        Supports:
        - async handlers;
        - sync handlers.

        """
        last_error = None
        for attempt in range(self._retry.attempts):
            try:
                await self._dispatcher.dispatch(handler, event)
                return
            except Exception as exc:
                last_error = exc
                await asyncio.sleep(self._retry.delay)

        if self._errors.dead_letter:
            self._errors.dead_letter(event, last_error)

        method = getattr(handler, "handle")
        result = method(event)

        if inspect.isawaitable(result):
            await result
