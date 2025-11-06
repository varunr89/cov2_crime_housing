import pytest
import logging
from pathlib import Path
from src.data.utils.logger import setup_logger, get_logger


class TestLogger:
    """Test logging utilities."""

    def test_setup_logger_creates_file(self, tmp_path):
        """Test that setup_logger creates log file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_logger',
            log_file=str(log_file),
            level=logging.INFO
        )

        assert log_file.exists()
        assert logger.level == logging.INFO

    def test_logger_writes_messages(self, tmp_path):
        """Test that logger writes messages to file."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_write',
            log_file=str(log_file),
            level=logging.INFO
        )

        test_message = "Test log message"
        logger.info(test_message)

        log_content = log_file.read_text()
        assert test_message in log_content
        assert "INFO" in log_content

    def test_logger_respects_level(self, tmp_path):
        """Test that logger respects log level."""
        log_file = tmp_path / "test.log"
        logger = setup_logger(
            name='test_level',
            log_file=str(log_file),
            level=logging.WARNING
        )

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")

        log_content = log_file.read_text()
        assert "Debug message" not in log_content
        assert "Info message" not in log_content
        assert "Warning message" in log_content

    def test_get_logger_returns_existing(self, tmp_path):
        """Test that get_logger returns existing logger."""
        log_file = tmp_path / "test.log"
        logger1 = setup_logger(
            name='shared_logger',
            log_file=str(log_file),
            level=logging.INFO
        )

        logger2 = get_logger('shared_logger')

        assert logger1 is logger2
