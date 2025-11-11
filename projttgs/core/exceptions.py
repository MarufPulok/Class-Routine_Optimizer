"""
Custom exceptions for the application.
Following SOLID principles - centralized exception handling.
"""
from typing import Optional, Dict, Any


class BaseApplicationException(Exception):
    """Base exception for all application-specific exceptions."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(BaseApplicationException):
    """Raised when validation fails."""
    pass


class NotFoundError(BaseApplicationException):
    """Raised when a requested resource is not found."""
    pass


class BusinessLogicError(BaseApplicationException):
    """Raised when business logic rules are violated."""
    pass


class RoutineGenerationError(BusinessLogicError):
    """Raised when routine generation fails."""
    pass


class DatabaseError(BaseApplicationException):
    """Raised when database operations fail."""
    pass


class AuthenticationError(BaseApplicationException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(BaseApplicationException):
    """Raised when authorization fails."""
    pass

