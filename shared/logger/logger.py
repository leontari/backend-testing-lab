"""
Public logger API.

Application code should use this class only.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING

from shared.logger.context import LogContext, current_context, set_context
from shared.logger.formatter import JsonFormatter

if TYPE_CHECKING:
    from collections.abc import Mapping

    from shared.logger.config import LoggerConfig


@dataclass(slots=True, frozen=True)
class Logger:
    """
    Application logger facade.

    Hides stdlib logging configuration.
    Normally should be registered as singleton in DI.

    """

    _logger: logging.Logger
    _fields: Mapping[str, object] = field(default_factory=dict)

    def bind(self, **fields: object) -> Logger:
        """
        Create logger with bound fields.

        Returns
        -------
        Logger
            Logger with additional context.

        """
        context = current_context()
        set_context(LogContext({**context.fields, **fields}))

        return Logger(
            self._logger,
            MappingProxyType({**self._fields, **fields}),
        )

    def info(self, message: str, **fields: object) -> None:
        """Write info message."""
        self._logger.info(message, extra=fields)

    def error(self, message: str, **fields: object) -> None:
        """Write error message."""
        self._logger.error(message, extra=fields)

    def exception(self, message: str, **fields: object) -> None:
        """Write exception message."""
        self._logger.exception(message, extra=fields)


def configure_logger(config: LoggerConfig) -> Logger:
    """
    Configure application logger.

    Used by composition root.

    Returns
    -------
    Logger
        Configured logger facade.

    """
    logger = logging.getLogger(config.service)
    logger.setLevel(config.level)
    handler = logging.StreamHandler()

    handler.setFormatter(
        JsonFormatter({
            "service": config.service,
            "environments": config.environment,
            "version": config.version,
        })
    )

    logger.handlers.clear()
    logger.addHandler(handler)

    return Logger(logger)


__all__ = (
    "Logger",
    "configure_logger",
)
