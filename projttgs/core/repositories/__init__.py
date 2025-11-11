"""
Repository pattern implementation.
Following Dependency Inversion Principle - depends on abstractions.
"""
from .base import BaseRepository
from .mongodb_repository import MongoDBRepository

__all__ = ['BaseRepository', 'MongoDBRepository']

