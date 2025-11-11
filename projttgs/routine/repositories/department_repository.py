"""
Department repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import Department


class DepartmentRepository(MongoDBRepository[Department]):
    """Repository for Department model."""
    
    def __init__(self):
        super().__init__(Department)

