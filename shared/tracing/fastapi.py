"""
FastAPI tracing middleware.

This middleware is responsible only for:

- extracting trace context from HTTP headers
- creating or restoring TraceContext
- binding it to ContextVar via TraceManager
- injecting trace headers into HTTP response

It does NOT:

- parse W3C trace format
- know anything about Kafka or gRPC
- contain business logic
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

from .transport.http import http_trace_adapter

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi import Request, Response
    from starlette.types import ASGIApp

    from .manager import TraceManager
    from .models import RawTraceCarrier


class TraceMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for distributed tracing propagation."""

    def __init__(
        self,
        app: ASGIApp,
        trace_manager: TraceManager,
    ) -> None:
        """
        Initialize middleware.

        Parameters
        ----------
        app:
            FastAPI application.

        trace_manager:
            Runtime trace manager.

        """
        super().__init__(app)
        self._trace_manager = trace_manager

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """
        Process incoming request with trace propagation.

        Parameters
        ----------
        request:
            Incoming HTTP request.

        call_next:
            Next ASGI handler.

        Returns
        -------
        Response
            HTTP response with trace headers injected.

        """
        # 1. Extract raw transport headers
        carrier = http_trace_adapter.extract(request.headers)

        # 2. Create or restore TraceContext
        if carrier is None:
            trace = self._trace_manager.create_root_trace()
        else:
            trace = self._trace_manager.create_remote_trace(carrier)

        # 3. Install context into ContextVar
        token = self._trace_manager.install_trace(trace)

        try:
            # 4. Process request
            response = await call_next(request)

            # 5. Inject trace into response headers
            updated_trace: RawTraceCarrier = trace.carrier
            response.headers.update(updated_trace.headers)

            return response

        finally:
            # 6. Always restore previous context
            self._trace_manager.restore_trace(token)
