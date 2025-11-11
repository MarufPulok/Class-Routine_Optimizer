"""
Timetable service for CRUD operations.
Following Single Responsibility Principle - handles timetable business logic only.
"""
from typing import List, Optional, Dict, Any
from routine.models import Section
from routine.repositories.section_repository import SectionRepository
from core.services.base import BaseService
from core.exceptions import NotFoundError, ValidationError


class TimetableService(BaseService):
    """
    Service for timetable operations.
    Following Dependency Inversion Principle - depends on repository abstraction.
    """
    
    def __init__(self, section_repository: SectionRepository = None):
        """
        Initialize service with repository dependency.
        
        Args:
            section_repository: Section repository instance
        """
        super().__init__()
        self.section_repository = section_repository or SectionRepository()
    
    def get_all_sections(self) -> List[Section]:
        """Get all sections."""
        return self.section_repository.get_all()
    
    def get_section_by_id(self, section_id: str) -> Section:
        """
        Get section by ID.
        
        Args:
            section_id: Section ID
            
        Returns:
            Section instance
            
        Raises:
            NotFoundError: If section not found
        """
        section = self.section_repository.get_by_id(section_id)
        if section is None:
            raise NotFoundError(f"Section with id {section_id} not found")
        return section
    
    def update_section_assignment(self, section_id: str, room_id: str = None,
                                  meeting_time_id: str = None,
                                  instructor_id: str = None) -> Section:
        """
        Update section assignments (room, meeting time, instructor).
        
        Args:
            section_id: Section ID
            room_id: Room ID (optional)
            meeting_time_id: Meeting time ID (optional)
            instructor_id: Instructor ID (optional)
            
        Returns:
            Updated section instance
        """
        section = self.get_section_by_id(section_id)
        
        if room_id:
            from routine.repositories.room_repository import RoomRepository
            room_repo = RoomRepository()
            room = room_repo.get_or_raise(room_id)
            section.set_room(room)
        
        if meeting_time_id:
            from routine.repositories.meeting_time_repository import MeetingTimeRepository
            mt_repo = MeetingTimeRepository()
            meeting_time = mt_repo.get_or_raise(meeting_time_id)
            section.set_meetingTime(meeting_time)
        
        if instructor_id:
            from routine.repositories.instructor_repository import InstructorRepository
            inst_repo = InstructorRepository()
            instructor = inst_repo.get_or_raise(instructor_id)
            section.set_instructor(instructor)
        
        return section

