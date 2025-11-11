"""
Section repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import Section


class SectionRepository(MongoDBRepository[Section]):
    """Repository for Section model."""
    
    def __init__(self):
        super().__init__(Section)

