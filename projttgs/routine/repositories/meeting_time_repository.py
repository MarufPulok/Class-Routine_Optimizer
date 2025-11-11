"""
MeetingTime repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import MeetingTime


class MeetingTimeRepository(MongoDBRepository[MeetingTime]):
    """Repository for MeetingTime model."""
    
    def __init__(self):
        super().__init__(MeetingTime)

