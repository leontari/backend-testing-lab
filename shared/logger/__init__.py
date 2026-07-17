"""Logger package."""
from __future__ import annotations

from shared.logger.config import LoggerConfig
from shared.logger.logger import Logger, configure_logger

__version__ = "0.1.0"

__all__ = (
    "Logger",
    "LoggerConfig",
    "__version__",
    "configure_logger",
)
