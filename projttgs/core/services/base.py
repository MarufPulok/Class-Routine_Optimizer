"""
Base service class.
Following Service Layer Pattern and Single Responsibility Principle.
"""
from abc import ABC
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base service class.
    All business logic services should inherit from this.
    Following Single Responsibility Principle - services contain only business logic.
    """
    
    def __init__(self):
        """Initialize the service."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def log_info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        self.logger.info(message, extra=kwargs)
    
    def log_error(self, message: str, error: Optional[Exception] = None, **kwargs) -> None:
        """Log an error message."""
        if error:
            self.logger.error(f"{message}: {str(error)}", exc_info=True, extra=kwargs)
        else:
            self.logger.error(message, extra=kwargs)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        self.logger.warning(message, extra=kwargs)

