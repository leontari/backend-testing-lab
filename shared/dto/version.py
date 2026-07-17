"""
DTO version definitions.

DTO versions allow backward compatible
transport contract evolution.
"""

from __future__ import annotations

from enum import IntEnum


class DTOVersion(IntEnum):
    """Supported DTO schema versions."""

    V1 = 1


__all__ = ("DTOVersion",)
