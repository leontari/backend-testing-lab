"""
FastAPI tracing middleware.

Uses public Tracing API only.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware

if TYPE_CHECKING:

    from collections.abc import Callable

    from fastapi import Request, Response
    from starlette.types import ASGIApp

    from .tracing import Tracing


class TraceMiddleware(BaseHTTPMiddleware):
    """FastAPI distributed tracing middleware."""

    def __init__(self, app: ASGIApp, tracing: Tracing) -> None:
        super().__init__(app)
        self._tracing = tracing

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        # Restore incoming distributed context
        source = self._tracing.extract(request.headers)

        # Create request span
        async with self._tracing.span(source) as context:
            response = await call_next(request)
            # Propagate current trace downstream
            self._tracing.inject(context, response.headers)

            return response


__all__ = ("TraceMiddleware",)
