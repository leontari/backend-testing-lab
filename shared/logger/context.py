"""
Logger runtime context.

Provides contextual metadata propagation.
Compatible with async applications.
"""

from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class LogContext:
    """
    Runtime logging context.

    Contains metadata attached to every log record.

    """

    fields: dict[str, object] = field(default_factory=dict)


_context: ContextVar[LogContext] = ContextVar(
    "logger_context",
    default=LogContext(),
)


def current_context() -> LogContext:
    """
    Get current logging context.

    Returns
    -------
    LogContext
        Current runtime context.

    """
    return _context.get()


def set_context(context: LogContext) -> Token[LogContext]:
    """
    Set current logging context.

    Returns
    -------
    Token
        Context restore token.

    """
    return _context.set(context)


def reset_context(token: Token) -> None:
    """Restore previous logging context."""
    _context.reset(token)


__all__ = (
    "LogContext",
    "current_context",
    "reset_context",
    "set_context",
)
