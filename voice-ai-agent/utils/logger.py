"""
Logging utilities for the Voice AI Agent.
"""
import logging
import sys
from datetime import datetime


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Setup a logger with console output.
    
    Args:
        name: Logger name
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger


# Module-level logger
logger = setup_logger("VoiceAIAgent")


def log_info(message: str):
    """Log info message."""
    logger.info(message)


def log_error(message: str):
    """Log error message."""
    logger.error(message)


def log_debug(message: str):
    """Log debug message."""
    logger.debug(message)
