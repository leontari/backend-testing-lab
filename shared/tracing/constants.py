"""
W3C Trace Context constants.

This module defines protocol-level constants used for propagation
of distributed tracing context across different transports:

- HTTP headers
- gRPC metadata
- Kafka message headers
- custom message carriers

The implementation follows the W3C Trace Context specification:

https://www.w3.org/TR/trace-context/

Currently supported specification version:

    W3C Trace Context version "00"

The module contains only protocol constants.
No parsing, validation or business logic should be implemented here.
"""

from __future__ import annotations

#########################################################
# HTTP/generic carrier header name for W3C trace context.
#########################################################
# The traceparent header contains the core distributed tracing
# information required to propagate a trace between services.
#
# Format:
#     version-trace-id-parent-id-trace-flags
#
# Example:
#     traceparent:
#     00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
#
# Fields:
#     version      -> Trace Context version
#     trace-id     -> globally unique trace identifier
#     parent-id    -> current span identifier
#     trace-flags  -> sampling and future control flags
#
TRACEPARENT_HEADER: str = "traceparent"


#################################
# Optional W3C tracestate header.
#################################
# The tracestate header carries vendor-specific tracing state.
#
# It is used together with traceparent and allows tracing systems
# to store additional implementation-specific information while
# preserving interoperability.
#
# Example:
#     tracestate:
#     vendor=value,vendor2=value2
#
# The core tracing implementation does not interpret tracestate
# values and only propagates them.
#
TRACESTATE_HEADER: str = "tracestate"


##############################################
# Current supported W3C Trace Context version.
##############################################
# The version is the first field of the traceparent header.
#
# Format:
#     {version}-{trace_id}-{span_id}-{flags}
#
# Example:
#     00-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-bbbbbbbbbbbbbbbb-01
#
# Version "00" is the first stable W3C Trace Context format.
#
TRACE_VERSION: str = "00"


###################
# Trace is sampled.
###################
# The sampling flag indicates that the trace should be recorded.
#
# Binary representation:
#     00000001
#
# Hex representation inside traceparent:
#     01
#
# Example:
#     00-trace_id-span_id-01
#
TRACE_FLAGS_SAMPLED: str = "01"


#######################
# Trace is not sampled.
#######################
# The trace context is still propagated between services,
# but tracing systems may skip storing/exporting spans.
#
# Binary representation:
#     00000000
#
# Hex representation inside traceparent:
#     00
#
# Example:
#     00-trace_id-span_id-00
#
TRACE_FLAGS_NOT_SAMPLED: str = "00"


##################
# Identifier Sizes
##################
# Trace ID size in hexadecimal characters.
#
# W3C specification:
#     trace-id = 16 bytes
#
# Hex encoding:
#     16 bytes * 2 characters = 32 characters
#
# Example:
#     4bf92f3577b34da6a3ce929d0e0e4736
#
# Requirements:
# - exactly 32 hexadecimal characters
# - must not contain only zeros
# - globally unique
#
TRACE_ID_LENGTH: int = 32

#########################################
# Span ID size in hexadecimal characters.
#########################################
# W3C specification:
#     parent-id = 8 bytes
#
# Hex encoding:
#     8 bytes * 2 characters = 16 characters
#
# Example:
#     00f067aa0ba902b7
#
# Requirements:
# - exactly 16 hexadecimal characters
# - must not contain only zeros
# - unique within a trace
#
SPAN_ID_LENGTH: int = 16

__all__ = (
    "SPAN_ID_LENGTH",
    "TRACEPARENT_HEADER",
    "TRACESTATE_HEADER",
    "TRACE_FLAGS_NOT_SAMPLED",
    "TRACE_FLAGS_SAMPLED",
    "TRACE_ID_LENGTH",
    "TRACE_VERSION",
)
