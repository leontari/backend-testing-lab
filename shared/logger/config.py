"""
Logger configuration.

Defines runtime configuration for application logging.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoggerConfig:
    """
    Logger runtime configuration.

    Parameters
    ----------
    service:
        Service name.
    environment:
        Runtime environment.
    version:
        Application version.
    level:
        Logging level.
    json:
        Enable JSON structured output.
    include_timestamp:
        Include timestamp in formatter output.

    """

    service: str = "application"
    environment: str = "development"
    version: str = "0.0.0"
    level: str = "INFO"
    json: bool = True
    include_timestamp: bool = True


__all__ = ("LoggerConfig",)
