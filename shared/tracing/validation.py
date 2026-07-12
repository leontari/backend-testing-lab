"""
Trace context validation rules.

This module contains domain validation only.
It does not create objects.

"""

from __future__ import annotations

import re

from shared.tracing.constants import (
    SPAN_ID_LENGTH,
    TRACE_FLAGS_NOT_SAMPLED,
    TRACE_FLAGS_SAMPLED,
    TRACE_ID_LENGTH,
    TRACE_VERSION,
)
from shared.tracing.exceptions import InvalidTraceContextError

_HEX_RE = re.compile(r"^[0-9a-f]+$")


def _validate_version(version: str) -> None:
    """Validate W3C trace version."""
    if len(version) != len(TRACE_VERSION):
        msg = "Trace version must contain exactly two hexadecimal characters."
        raise InvalidTraceContextError(msg)

    if not _HEX_RE.fullmatch(version):
        msg = "Trace version must be hexadecimal."
        raise InvalidTraceContextError(msg)


def _validate_trace_id(trace_id: str) -> None:
    """Validate trace identifier."""
    if len(trace_id) != TRACE_ID_LENGTH:
        msg = (
            f"Invalid trace_id length "
            f"({len(trace_id)}). "
            f"Expected {TRACE_ID_LENGTH}."
        )
        raise InvalidTraceContextError(msg)

    if not _HEX_RE.fullmatch(trace_id):
        msg = "trace_id must contain hexadecimal characters only."
        raise InvalidTraceContextError(msg)

    if int(trace_id, 16) == 0:
        msg = "trace_id cannot be all zeros."
        raise InvalidTraceContextError(msg)


def _validate_span_id(span_id: str) -> None:
    """Validate span identifier."""
    if len(span_id) != SPAN_ID_LENGTH:
        msg = (
            f"Invalid span_id length "
            f"({len(span_id)}). "
            f"Expected {SPAN_ID_LENGTH}."
        )
        raise InvalidTraceContextError(msg)

    if not _HEX_RE.fullmatch(span_id):
        msg = "span_id must contain hexadecimal characters only."
        raise InvalidTraceContextError(msg)

    if int(span_id, 16) == 0:
        msg = "span_id cannot be all zeros."
        raise InvalidTraceContextError(msg)


def _validate_parent_span_id(span_id: str | None) -> None:
    """
    Validate parents span id.

    None is allowed for root spans.
    """
    if span_id is None:
        return None

    return _validate_span_id(span_id)


def _validate_trace_flags(trace_flags: str) -> None:
    """Validate trace sampling flags."""
    if trace_flags not in {
        TRACE_FLAGS_SAMPLED,
        TRACE_FLAGS_NOT_SAMPLED,
    }:
        msg = "Unsupported trace_flags value."
        raise InvalidTraceContextError(msg)


def validate_trace_context(
    *,
    version: str,
    trace_id: str,
    span_id: str,
    parent_span_id: str | None,
    trace_flags: str,
) -> None:
    """Validate TraceContext fields before creation."""
    _validate_version(version)
    _validate_trace_id(trace_id)
    _validate_span_id(span_id)
    _validate_parent_span_id(parent_span_id)
    _validate_trace_flags(trace_flags)


__all__ = ("validate_trace_context",)
