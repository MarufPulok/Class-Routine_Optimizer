"""
Room repository implementation.
"""
from core.repositories.mongodb_repository import MongoDBRepository
from routine.models import Room


class RoomRepository(MongoDBRepository[Room]):
    """Repository for Room model."""
    
    def __init__(self):
        super().__init__(Room)

