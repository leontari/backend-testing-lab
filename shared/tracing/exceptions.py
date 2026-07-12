"""
Tracing domain exceptions.

Used across propagators, managers and runtime storage.

"""

from __future__ import annotations


class TraceError(Exception):
    """Base exception for all tracing-related errors."""


class TraceContextMissingError(TraceError):
    """
    Raised when TraceContext is requested but not initialized.

    Typical scenario:
        - middleware not installed
        - missing root trace creation
    """


class InvalidTraceContextError(TraceError):
    """
    Invalid TraceContext error.

    Raised when `traceparent` header does not match W3C specification.
    """


class InvalidTraceStateError(TraceError):
    """Raised when `tracestate` header cannot be parsed."""


__all__ = (
    "InvalidTraceContextError",
    "InvalidTraceStateError",
    "TraceContextMissingError",
    "TraceError",
)
