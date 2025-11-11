"""
Course repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import Course


class CourseRepository(MongoDBRepository[Course]):
    """Repository for Course model."""
    
    def __init__(self):
        super().__init__(Course)

