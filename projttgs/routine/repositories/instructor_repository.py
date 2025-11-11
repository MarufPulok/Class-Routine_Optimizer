"""
Instructor repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import Instructor


class InstructorRepository(MongoDBRepository[Instructor]):
    """Repository for Instructor model."""
    
    def __init__(self):
        super().__init__(Instructor)

