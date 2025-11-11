"""
MongoDB repository implementation using mongoengine.
Following Repository Pattern - concrete implementation of BaseRepository.
"""
from typing import Optional, List, Dict, Any
from mongoengine import Document, DoesNotExist

from core.repositories.base import BaseRepository, ModelType
from core.exceptions import NotFoundError, DatabaseError


class MongoDBRepository(BaseRepository[ModelType]):
    """
    MongoDB repository implementation using mongoengine.
    Provides CRUD operations for MongoDB models.
    """
    
    def get_by_id(self, pk: Any) -> Optional[ModelType]:
        """
        Retrieve a single instance by primary key.
        
        Args:
            pk: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        try:
            return self.model.objects.get(pk=pk)
        except DoesNotExist:
            return None
        except Exception as e:
            raise DatabaseError(f"Error retrieving {self.model.__name__}: {str(e)}")
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[ModelType]:
        """
        Retrieve all instances, optionally filtered.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            List of model instances
        """
        try:
            queryset = self.model.objects
            if filters:
                queryset = queryset.filter(**filters)
            return list(queryset)
        except Exception as e:
            raise DatabaseError(f"Error retrieving {self.model.__name__} list: {str(e)}")
    
    def create(self, **kwargs) -> ModelType:
        """
        Create a new instance.
        
        Args:
            **kwargs: Model field values
            
        Returns:
            Created model instance
        """
        try:
            return self.model(**kwargs).save()
        except Exception as e:
            raise DatabaseError(f"Error creating {self.model.__name__}: {str(e)}")
    
    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """
        Update an existing instance.
        
        Args:
            instance: Model instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated model instance
        """
        try:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except Exception as e:
            raise DatabaseError(f"Error updating {self.model.__name__}: {str(e)}")
    
    def delete(self, instance: ModelType) -> None:
        """
        Delete an instance.
        
        Args:
            instance: Model instance to delete
        """
        try:
            instance.delete()
        except Exception as e:
            raise DatabaseError(f"Error deleting {self.model.__name__}: {str(e)}")
    
    def filter(self, **kwargs) -> List[ModelType]:
        """
        Filter instances by criteria.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            List of filtered model instances
        """
        try:
            return list(self.model.objects.filter(**kwargs))
        except Exception as e:
            raise DatabaseError(f"Error filtering {self.model.__name__}: {str(e)}")
    
    def exists(self, **kwargs) -> bool:
        """
        Check if instances matching criteria exist.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            True if any instances exist, False otherwise
        """
        try:
            return self.model.objects.filter(**kwargs).count() > 0
        except Exception as e:
            raise DatabaseError(f"Error checking existence of {self.model.__name__}: {str(e)}")
