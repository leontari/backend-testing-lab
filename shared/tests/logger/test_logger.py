from __future__ import annotations

import logging

from shared.logger.config import LoggerConfig
from shared.logger.logger import Logger, configure_logger


def test_configure_logger() -> None:
    """Logger should be created from config."""
    logger = configure_logger(LoggerConfig(service="test"))
    assert isinstance(logger, Logger)


def test_logger_info(caplog) -> None:
    """Logger should emit info messages."""
    logger = configure_logger(LoggerConfig(service="test"))
    with caplog.at_level(logging.INFO):
        logger.info("hello", user_id=10)

    assert any("hello" in record.message for record in caplog.records)


def test_logger_error(caplog) -> None:
    """Logger should emit errors."""
    logger = configure_logger(LoggerConfig())
    with caplog.at_level(logging.ERROR):
        logger.error("failed")

    assert any(record.levelname == "ERROR" for record in caplog.records)


def test_logger_exception(caplog) -> None:
    """Logger should write exceptions."""
    logger = configure_logger(LoggerConfig())
    with caplog.at_level(logging.ERROR):
        try:
            raise RuntimeError("boom")
        except RuntimeError:
            logger.exception("operation failed")

    assert any(
        "operation failed" in record.message for record in caplog.records
    )


def test_logger_bind() -> None:
    """Bind should create new immutable logger instance."""
    logger = configure_logger(LoggerConfig())
    result = logger.bind(request_id="123")

    assert result is not logger
    assert result._fields["request_id"] == "123"


def test_logger_original_context_not_modified() -> None:
    """Original logger must stay unchanged after bind."""
    logger = configure_logger(LoggerConfig())
    logger.bind(request_id="123")

    assert logger._fields == {}


def test_logger_bind_isolated() -> None:
    """Bound loggers must not share mutable state."""
    logger = configure_logger(LoggerConfig())
    request_logger = logger.bind(request_id="123")
    payment_logger = logger.bind(payment_id="456")

    assert request_logger._fields == {"request_id": "123"}
    assert payment_logger._fields == {"payment_id": "456"}
    assert logger._fields == {}
