"""
DTO exceptions.

Contains exceptions related to DTO lifecycle,
serialization and registration.
"""
from __future__ import annotations


class DTOError(Exception):
    """Base DTO exception."""


class DTORegistrationError(DTOError):
    """
    Raised when DTO registration fails.

    Examples:
    - duplicate DTO name/version;
    - invalid DTO type.

    """


class DTOSerializationError(DTOError):
    """Raised when DTO serialization or deserialization fails."""
