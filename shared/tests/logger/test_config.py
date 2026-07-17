from __future__ import annotations

from shared.logger.config import LoggerConfig


def test_default_config() -> None:
    """LoggerConfig should provide safe defaults."""

    config = LoggerConfig()

    assert config.service == "application"
    assert config.environment == "development"
    assert config.version == "0.0.0"
    assert config.level == "INFO"
    assert config.json is True


def test_config_is_immutable() -> None:
    """LoggerConfig must be frozen."""

    config = LoggerConfig()

    try:
        config.level = "DEBUG"

    except AttributeError:
        pass

    else:
        msg = "LoggerConfig must be immutable"
        raise AssertionError(msg)
