"""
DRF views for routine app.
Following Single Responsibility Principle - views handle HTTP request/response only.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from routine.models import Room, Instructor, MeetingTime, Course, Department, Section
from routine.serializers import (
    RoomSerializer, InstructorSerializer, MeetingTimeSerializer,
    CourseSerializer, DepartmentSerializer, SectionSerializer,
    RoutineGenerationSerializer, TimetableSerializer
)
from routine.repositories import (
    RoomRepository, InstructorRepository, MeetingTimeRepository,
    CourseRepository, DepartmentRepository, SectionRepository
)
from routine.services.routine_generation_service import RoutineGenerationService
from routine.services.pdf_generation_service import PDFGenerationService
from core.exceptions import NotFoundError, ValidationError, RoutineGenerationError


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Room CRUD operations.
    Following Dependency Inversion Principle - uses repository.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = RoomRepository()


class InstructorViewSet(viewsets.ModelViewSet):
    """ViewSet for Instructor CRUD operations."""
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = InstructorRepository()


class MeetingTimeViewSet(viewsets.ModelViewSet):
    """ViewSet for MeetingTime CRUD operations."""
    queryset = MeetingTime.objects.all()
    serializer_class = MeetingTimeSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = MeetingTimeRepository()


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course CRUD operations."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = CourseRepository()


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = DepartmentRepository()


class SectionViewSet(viewsets.ModelViewSet):
    """ViewSet for Section CRUD operations."""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SectionRepository()


class RoutineGenerationView(APIView):
    """
    API endpoint for routine generation.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RoutineGenerationSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generation_service = RoutineGenerationService()
    
    def post(self, request):
        """
        Generate routine/timetable.
        
        POST /api/routine/generate/
        """
        serializer = RoutineGenerationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = self.generation_service.generate_routine(
                strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                population_size=serializer.validated_data.get('population_size', 9),
                max_generations=serializer.validated_data.get('max_generations', 1000),
                mutation_rate=serializer.validated_data.get('mutation_rate', 0.1),
            )
            
            response_serializer = TimetableSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except RoutineGenerationError as e:
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': 'Routine generation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RoutinePDFGenerationView(APIView):
    """
    API endpoint for PDF generation of routine.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RoutineGenerationSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generation_service = RoutineGenerationService()
        self.pdf_service = PDFGenerationService()
    
    def post(self, request):
        """
        Generate routine and return as PDF.
        
        POST /api/routine/generate-pdf/
        """
        serializer = RoutineGenerationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Generate routine
            result = self.generation_service.generate_routine(
                strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                population_size=serializer.validated_data.get('population_size', 9),
                max_generations=serializer.validated_data.get('max_generations', 1000),
                mutation_rate=serializer.validated_data.get('mutation_rate', 0.1),
            )
            
            # Generate PDF
            return self.pdf_service.create_pdf_response(result, filename='routine.pdf')
        except RoutineGenerationError as e:
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'error': 'PDF generation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
