"""
Dashboard service for calculating statistics and metrics.
Following Single Responsibility Principle - handles dashboard data aggregation only.
"""
from typing import Dict, Any, List
from core.services.base import BaseService
from routine.repositories import (
    RoomRepository, InstructorRepository, MeetingTimeRepository,
    CourseRepository, DepartmentRepository, SectionRepository,
    GenerationHistoryRepository
)


class DashboardService(BaseService):
    """
    Service for dashboard statistics and metrics.
    Following Dependency Inversion Principle - uses repository abstractions.
    """
    
    def __init__(self):
        """Initialize dashboard service with repositories."""
        super().__init__()
        self.room_repo = RoomRepository()
        self.instructor_repo = InstructorRepository()
        self.meeting_time_repo = MeetingTimeRepository()
        self.course_repo = CourseRepository()
        self.department_repo = DepartmentRepository()
        self.section_repo = SectionRepository()
        self.generation_history_repo = GenerationHistoryRepository()
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard statistics.
        
        Returns:
            Dictionary with counts, assignments, utilization, readiness, and generation history
        """
        counts = self._calculate_counts()
        assignments = self._calculate_assignments()
        utilization = self._calculate_utilization()
        readiness = self._check_readiness()
        generation_history = self._get_generation_history_stats()
        
        return {
            'counts': counts,
            'assignments': assignments,
            'utilization': utilization,
            'readiness': readiness,
            'generation_history': generation_history
        }
    
    def _calculate_counts(self) -> Dict[str, Any]:
        """Calculate entity counts."""
        rooms = self.room_repo.get_all()
        instructors = self.instructor_repo.get_all()
        courses = self.course_repo.get_all()
        departments = self.department_repo.get_all()
        sections = self.section_repo.get_all()
        meeting_times = self.meeting_time_repo.get_all()
        
        total_seating_capacity = sum(room.seating_capacity for room in rooms)
        
        return {
            'rooms': len(rooms),
            'instructors': len(instructors),
            'courses': len(courses),
            'departments': len(departments),
            'sections': len(sections),
            'meeting_times': len(meeting_times),
            'total_seating_capacity': total_seating_capacity
        }
    
    def _calculate_assignments(self) -> Dict[str, Any]:
        """Calculate section assignment statistics."""
        sections = self.section_repo.get_all()
        
        total_sections = len(sections)
        assigned_sections = 0
        partially_assigned_sections = 0
        unassigned_sections = 0
        
        for section in sections:
            has_room = section.room is not None
            has_instructor = section.instructor is not None
            has_meeting_time = section.meeting_time is not None
            
            assignment_count = sum([has_room, has_instructor, has_meeting_time])
            
            if assignment_count == 3:
                assigned_sections += 1
            elif assignment_count == 0:
                unassigned_sections += 1
            else:
                partially_assigned_sections += 1
        
        completion_percentage = (
            (assigned_sections / total_sections * 100) if total_sections > 0 else 0.0
        )
        
        return {
            'total_sections': total_sections,
            'assigned_sections': assigned_sections,
            'partially_assigned_sections': partially_assigned_sections,
            'unassigned_sections': unassigned_sections,
            'completion_percentage': round(completion_percentage, 2)
        }
    
    def _calculate_utilization(self) -> Dict[str, Any]:
        """Calculate utilization metrics."""
        sections = self.section_repo.get_all()
        rooms = self.room_repo.get_all()
        instructors = self.instructor_repo.get_all()
        meeting_times = self.meeting_time_repo.get_all()
        
        # Room utilization
        room_utilization = {}
        for room in rooms:
            room_sections = [s for s in sections if s.room and s.room.id == room.id]
            utilization_percentage = (
                (len(room_sections) / room.seating_capacity * 100) if room.seating_capacity > 0 else 0.0
            )
            room_utilization[room.r_number] = {
                'sections': len(room_sections),
                'capacity': room.seating_capacity,
                'utilization_percentage': round(utilization_percentage, 2)
            }
        
        # Instructor workload
        instructor_workload = {}
        for instructor in instructors:
            instructor_sections = [
                s for s in sections if s.instructor and s.instructor.id == instructor.id
            ]
            instructor_workload[instructor.uid] = len(instructor_sections)
        
        # Time slot distribution
        time_slot_distribution = {}
        day_distribution = {}
        
        for meeting_time in meeting_times:
            mt_sections = [
                s for s in sections if s.meeting_time and s.meeting_time.id == meeting_time.id
            ]
            time_slot_distribution[meeting_time.pid] = len(mt_sections)
            
            # Day-wise distribution
            day = meeting_time.day
            if day not in day_distribution:
                day_distribution[day] = 0
            day_distribution[day] += len(mt_sections)
        
        return {
            'room_utilization': room_utilization,
            'instructor_workload': instructor_workload,
            'time_slot_distribution': time_slot_distribution,
            'day_distribution': day_distribution
        }
    
    def _check_readiness(self) -> Dict[str, Any]:
        """Check if system is ready for routine generation."""
        counts = self._calculate_counts()
        missing_items = []
        
        if counts['rooms'] == 0:
            missing_items.append('rooms')
        if counts['instructors'] == 0:
            missing_items.append('instructors')
        if counts['meeting_times'] == 0:
            missing_items.append('meeting_times')
        if counts['courses'] == 0:
            missing_items.append('courses')
        if counts['departments'] == 0:
            missing_items.append('departments')
        if counts['sections'] == 0:
            missing_items.append('sections')
        
        return {
            'ready': len(missing_items) == 0,
            'missing_items': missing_items
        }
    
    def _get_generation_history_stats(self) -> Dict[str, Any]:
        """Get generation history statistics."""
        stats = self.generation_history_repo.get_statistics()
        recent_generations = self.generation_history_repo.get_latest(limit=5)
        
        recent_list = []
        for gen in recent_generations:
            recent_list.append({
                'timestamp': gen.timestamp.isoformat(),
                'fitness_score': gen.fitness_score,
                'conflicts_count': gen.conflicts_count,
                'generations_run': gen.generations_run,
                'status': gen.status,
                'strategy_type': gen.strategy_type
            })
        
        return {
            'total_generations': stats['total_generations'],
            'average_fitness': round(stats['average_fitness'], 2),
            'best_fitness': round(stats['best_fitness'], 2),
            'average_conflicts': round(stats['average_conflicts'], 2),
            'success_count': stats['success_count'],
            'failed_count': stats['failed_count'],
            'recent_generations': recent_list
        }
    
    def get_section_status(self) -> Dict[str, Any]:
        """
        Get detailed section assignment status.
        
        Returns:
            Dictionary with section status breakdown by department
        """
        sections = self.section_repo.get_all()
        departments = self.department_repo.get_all()
        
        fully_assigned = 0
        partially_assigned = 0
        unassigned = 0
        
        by_department = {}
        
        for department in departments:
            dept_sections = [s for s in sections if s.department and s.department.id == department.id]
            
            dept_fully = 0
            dept_partial = 0
            dept_unassigned = 0
            
            for section in dept_sections:
                has_room = section.room is not None
                has_instructor = section.instructor is not None
                has_meeting_time = section.meeting_time is not None
                
                assignment_count = sum([has_room, has_instructor, has_meeting_time])
                
                if assignment_count == 3:
                    fully_assigned += 1
                    dept_fully += 1
                elif assignment_count == 0:
                    unassigned += 1
                    dept_unassigned += 1
                else:
                    partially_assigned += 1
                    dept_partial += 1
            
            by_department[department.dept_name] = {
                'total': len(dept_sections),
                'fully_assigned': dept_fully,
                'partially_assigned': dept_partial,
                'unassigned': dept_unassigned
            }
        
        return {
            'fully_assigned': fully_assigned,
            'partially_assigned': partially_assigned,
            'unassigned': unassigned,
            'by_department': by_department
        }

