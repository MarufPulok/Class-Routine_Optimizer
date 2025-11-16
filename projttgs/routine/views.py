"""
DRF views for routine app.
Following Single Responsibility Principle - views handle HTTP request/response only.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from mongoengine.errors import NotUniqueError, ValidationError as MongoValidationError

from routine.models import Room, Instructor, MeetingTime, Course, Department, Section
from routine.serializers import (
    RoomSerializer, InstructorSerializer, MeetingTimeSerializer,
    CourseSerializer, DepartmentSerializer, SectionSerializer,
    RoutineGenerationSerializer, TimetableSerializer,
    DashboardStatsSerializer, SectionStatusSerializer, GenerationHistorySerializer
)
from routine.repositories import (
    RoomRepository, InstructorRepository, MeetingTimeRepository,
    CourseRepository, DepartmentRepository, SectionRepository
)
from routine.repositories.generation_history_repository import GenerationHistoryRepository
from routine.services.routine_generation_service import RoutineGenerationService
from routine.services.pdf_generation_service import PDFGenerationService
from routine.services.dashboard_service import DashboardService
from core.exceptions import NotFoundError, ValidationError, RoutineGenerationError
from datetime import datetime


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
    
    def create(self, request, *args, **kwargs):
        """Create a room with proper error handling."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except NotUniqueError as e:
            # Handle duplicate room number
            error_msg = str(e)
            if 'r_number' in error_msg:
                return Response(
                    {'error': 'A room with this room number already exists.', 'r_number': ['Room number must be unique.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Duplicate entry. This room already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except MongoValidationError as e:
            return Response(
                {'error': 'Validation error', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to create room', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def update(self, request, *args, **kwargs):
        """Update a room with proper error handling."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_update(serializer)
            return Response(serializer.data)
        except NotUniqueError as e:
            # Handle duplicate room number
            error_msg = str(e)
            if 'r_number' in error_msg:
                return Response(
                    {'error': 'A room with this room number already exists.', 'r_number': ['Room number must be unique.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Duplicate entry. This room already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except MongoValidationError as e:
            return Response(
                {'error': 'Validation error', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to update room', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            
            # Save generation history
            history_repo = GenerationHistoryRepository()
            history_repo.create(
                timestamp=datetime.utcnow(),
                fitness_score=result.get('fitness', 0.0),
                conflicts_count=result.get('conflicts', 0),
                generations_run=result.get('generations', 0),
                status='Success',
                strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                parameters={
                    'population_size': serializer.validated_data.get('population_size', 9),
                    'max_generations': serializer.validated_data.get('max_generations', 1000),
                    'mutation_rate': serializer.validated_data.get('mutation_rate', 0.1),
                },
                created_by=request.user.username if hasattr(request.user, 'username') else None
            )
            
            response_serializer = TimetableSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except RoutineGenerationError as e:
            # Save failed generation history
            try:
                history_repo = GenerationHistoryRepository()
                history_repo.create(
                    timestamp=datetime.utcnow(),
                    fitness_score=0.0,
                    conflicts_count=0,
                    generations_run=0,
                    status='Failed',
                    strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                    parameters={
                        'population_size': serializer.validated_data.get('population_size', 9),
                        'max_generations': serializer.validated_data.get('max_generations', 1000),
                        'mutation_rate': serializer.validated_data.get('mutation_rate', 0.1),
                    },
                    created_by=request.user.username if hasattr(request.user, 'username') else None
                )
            except Exception:
                pass  # Don't fail if history save fails
            
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Save failed generation history
            try:
                history_repo = GenerationHistoryRepository()
                history_repo.create(
                    timestamp=datetime.utcnow(),
                    fitness_score=0.0,
                    conflicts_count=0,
                    generations_run=0,
                    status='Failed',
                    strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                    parameters=serializer.validated_data,
                    created_by=request.user.username if hasattr(request.user, 'username') else None
                )
            except Exception:
                pass  # Don't fail if history save fails
            
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
            
            # Save generation history
            history_repo = GenerationHistoryRepository()
            history_repo.create(
                timestamp=datetime.utcnow(),
                fitness_score=result.get('fitness', 0.0),
                conflicts_count=result.get('conflicts', 0),
                generations_run=result.get('generations', 0),
                status='Success',
                strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                parameters={
                    'population_size': serializer.validated_data.get('population_size', 9),
                    'max_generations': serializer.validated_data.get('max_generations', 1000),
                    'mutation_rate': serializer.validated_data.get('mutation_rate', 0.1),
                },
                created_by=request.user.username if hasattr(request.user, 'username') else None
            )
            
            # Generate PDF
            return self.pdf_service.create_pdf_response(result, filename='routine.pdf')
        except RoutineGenerationError as e:
            # Save failed generation history
            try:
                history_repo = GenerationHistoryRepository()
                history_repo.create(
                    timestamp=datetime.utcnow(),
                    fitness_score=0.0,
                    conflicts_count=0,
                    generations_run=0,
                    status='Failed',
                    strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                    parameters={
                        'population_size': serializer.validated_data.get('population_size', 9),
                        'max_generations': serializer.validated_data.get('max_generations', 1000),
                        'mutation_rate': serializer.validated_data.get('mutation_rate', 0.1),
                    },
                    created_by=request.user.username if hasattr(request.user, 'username') else None
                )
            except Exception:
                pass  # Don't fail if history save fails
            
            return Response(
                {'error': str(e.message)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Save failed generation history
            try:
                history_repo = GenerationHistoryRepository()
                history_repo.create(
                    timestamp=datetime.utcnow(),
                    fitness_score=0.0,
                    conflicts_count=0,
                    generations_run=0,
                    status='Failed',
                    strategy_type=serializer.validated_data.get('strategy_type', 'genetic_algorithm'),
                    parameters=serializer.validated_data,
                    created_by=request.user.username if hasattr(request.user, 'username') else None
                )
            except Exception:
                pass  # Don't fail if history save fails
            
            return Response(
                {'error': 'PDF generation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardStatsView(APIView):
    """
    API endpoint for dashboard statistics.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService()
    
    def get(self, request):
        """
        Get dashboard statistics.
        
        GET /api/routine/dashboard/stats/
        """
        try:
            stats = self.dashboard_service.get_dashboard_stats()
            serializer = DashboardStatsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch dashboard statistics'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SectionStatusView(APIView):
    """
    API endpoint for section assignment status.
    Following Dependency Inversion Principle - depends on service abstraction.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dashboard_service = DashboardService()
    
    def get(self, request):
        """
        Get section assignment status.
        
        GET /api/routine/sections/status/
        """
        try:
            status_data = self.dashboard_service.get_section_status()
            serializer = SectionStatusSerializer(status_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch section status'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerationHistoryView(APIView):
    """
    API endpoint for generation history.
    Following Dependency Inversion Principle - depends on repository abstraction.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_repo = GenerationHistoryRepository()
    
    def get(self, request):
        """
        Get generation history.
        
        GET /api/routine/dashboard/generation-history/
        Query params: limit, offset, date_from, date_to
        """
        try:
            limit = int(request.query_params.get('limit', 20))
            offset = int(request.query_params.get('offset', 0))
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            
            if date_from or date_to:
                from datetime import datetime
                date_from_obj = datetime.fromisoformat(date_from) if date_from else None
                date_to_obj = datetime.fromisoformat(date_to) if date_to else None
                history = self.history_repo.get_by_date_range(date_from_obj, date_to_obj)
            else:
                history = self.history_repo.get_latest(limit=limit + offset)
            
            # Apply pagination
            paginated_history = history[offset:offset + limit]
            
            serializer = GenerationHistorySerializer(paginated_history, many=True)
            return Response({
                'count': len(history),
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch generation history'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
