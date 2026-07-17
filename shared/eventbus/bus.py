"""
Application EventBus.

EventBus provides asynchronous parallel event notification.

EventBus does not:
- execute workflows;
- control business transactions;
- retry;
- persist messages.

Error handling should be implemented through middleware or transport layer.

"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from shared.eventbus.dispatcher import EventDispatcher
from shared.eventbus.exceptions import (
    EventDispatchError,
    HandlerNotFoundError,
)
from shared.eventbus.registry import EventRegistry

if TYPE_CHECKING:
    from shared.messaging import Event


@dataclass(slots=True)
class EventBus:
    """
    Parallel event notification bus.

    Example:
        PaymentCompleted

              |
       +------+------+------+

       Email  Slack  Metrics


    Handlers execute independently.
    Failure of one handler does not stop others.

    """

    _registry: EventRegistry = field(default_factory=EventRegistry)
    _dispatcher: EventDispatcher = field(default_factory=EventDispatcher)

    async def publish(self, event: Event) -> None:
        """
        Publish event.

        All handlers execute concurrently.

        Parameters
        ----------
        event:
            Event instance.

        Raises
        ------
        HandlerNotFoundError
            No subscribers.

        """
        handlers = self._registry.resolve(type(event))

        if not handlers:
            msg = f"No handlers for {type(event).__name__}"
            raise HandlerNotFoundError(msg)

        results = await asyncio.gather(
            *[
                self._dispatcher.dispatch(handler, event)
                for handler in handlers
            ]
        )

        errors = [
            result for result in results if isinstance(result, Exception)
        ]

        if errors:
            msg = f"{len(errors)} handlers failed"
            raise EventDispatchError(msg) from errors[0]

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
