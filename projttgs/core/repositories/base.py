"""
Abstract base repository interface.
Following Repository Pattern and Interface Segregation Principle.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from django.db import models

from core.exceptions import NotFoundError

ModelType = TypeVar('ModelType', bound=models.Model)


class BaseRepository(ABC, Generic[ModelType]):
    """
    Abstract base repository interface.
    Defines the contract for all repository implementations.
    Following Interface Segregation Principle - separate read/write operations.
    """
    
    def __init__(self, model: type[ModelType]):
        """
        Initialize repository with a model class.
        
        Args:
            model: Django model class
        """
        self.model = model
    
    @abstractmethod
    def get_by_id(self, pk: Any) -> Optional[ModelType]:
        """
        Retrieve a single instance by primary key.
        
        Args:
            pk: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """
        Retrieve all instances, optionally filtered.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            List of model instances
        """
        pass
    
    @abstractmethod
    def create(self, **kwargs) -> ModelType:
        """
        Create a new instance.
        
        Args:
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        pass
    
    @abstractmethod
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        Update an existing instance.
        
        Args:
            instance: Model instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated model instance
        """
        pass
    
    @abstractmethod
    def delete(self, instance: ModelType) -> None:
        """
        Delete an instance.
        
        Args:
            instance: Model instance to delete
        """
        pass
    
    def get_or_raise(self, pk: Any) -> ModelType:
        """
        Retrieve instance by ID or raise NotFoundError.
        
        Args:
            pk: Primary key value
            
        Returns:
            Model instance
            
        Raises:
            NotFoundError: If instance not found
        """
        instance = self.get_by_id(pk)
        if instance is None:
            raise NotFoundError(f"{self.model.__name__} with id {pk} not found")
        return instance

