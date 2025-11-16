"""
DRF serializers for routine app.
Following DTO Pattern - separate domain models from API representation.
"""
from rest_framework import serializers
from routine.models import (
    Room, Instructor, MeetingTime, Course, Department, Section
)


class RoomSerializer(serializers.Serializer):
    """Serializer for Room model."""
    id = serializers.CharField(read_only=True)
    r_number = serializers.CharField(max_length=6, required=True)
    seating_capacity = serializers.IntegerField(default=50, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new Room instance."""
        return Room.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update an existing Room instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class InstructorSerializer(serializers.Serializer):
    """Serializer for Instructor model."""
    id = serializers.CharField(read_only=True)
    uid = serializers.CharField(max_length=6, required=True)
    name = serializers.CharField(max_length=25, required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new Instructor instance."""
        return Instructor.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update an existing Instructor instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MeetingTimeSerializer(serializers.Serializer):
    """Serializer for MeetingTime model."""
    pid = serializers.CharField(max_length=5, required=True)
    time = serializers.ChoiceField(
        choices=[
            ('9:00 - 10:00', '9:00 - 10:00'),
            ('10:00 - 11:00', '10:00 - 11:00'),
            ('11:00 - 12:00', '11:00 - 12:00'),
            ('12:00 - 1:00', '12:00 - 1:00'),
            ('2:00 - 3:00', '2:00 - 3:00'),
            ('3:00 - 4:00', '3:00 - 4:00'),
            ('4:00 - 5:00', '4:00 - 5:00'),
        ],
        default='11:00 - 12:00',
        required=False
    )
    day = serializers.ChoiceField(
        choices=[
            ('Sunday', 'Sunday'),
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
        ],
        required=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new MeetingTime instance."""
        return MeetingTime.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """Update an existing MeetingTime instance."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CourseSerializer(serializers.Serializer):
    """Serializer for Course model."""
    course_number = serializers.CharField(max_length=8, required=True)
    course_name = serializers.CharField(max_length=40, required=True)
    max_numb_students = serializers.CharField(max_length=65, required=True)
    instructors = InstructorSerializer(many=True, read_only=True)
    instructor_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of instructor UIDs"
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new Course instance."""
        instructor_ids = validated_data.pop('instructor_ids', [])
        course = Course.objects.create(**validated_data)
        if instructor_ids:
            instructors = Instructor.objects.filter(uid__in=instructor_ids)
            course.instructors = list(instructors)
            course.save()
        return course
    
    def update(self, instance, validated_data):
        """Update an existing Course instance."""
        instructor_ids = validated_data.pop('instructor_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if instructor_ids is not None:
            instructors = Instructor.objects.filter(uid__in=instructor_ids)
            instance.instructors = list(instructors)
        instance.save()
        return instance


class DepartmentSerializer(serializers.Serializer):
    """Serializer for Department model."""
    id = serializers.CharField(read_only=True)
    dept_name = serializers.CharField(max_length=50, required=True)
    courses = CourseSerializer(many=True, read_only=True)
    course_ids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="List of course numbers"
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new Department instance."""
        course_ids = validated_data.pop('course_ids', [])
        department = Department.objects.create(**validated_data)
        if course_ids:
            courses = Course.objects.filter(course_number__in=course_ids)
            department.courses = list(courses)
            department.save()
        return department
    
    def update(self, instance, validated_data):
        """Update an existing Department instance."""
        course_ids = validated_data.pop('course_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if course_ids is not None:
            courses = Course.objects.filter(course_number__in=course_ids)
            instance.courses = list(courses)
        instance.save()
        return instance


class SectionSerializer(serializers.Serializer):
    """Serializer for Section model."""
    section_id = serializers.CharField(max_length=25, required=True)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Department name"
    )
    num_class_in_week = serializers.IntegerField(default=0, required=False)
    course = CourseSerializer(read_only=True)
    course_id = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Course number"
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Room number"
    )
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Instructor UID"
    )
    meeting_time = MeetingTimeSerializer(read_only=True)
    meeting_time_id = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Meeting time PID"
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """Create a new Section instance."""
        department_id = validated_data.pop('department_id')
        course_id = validated_data.pop('course_id', None)
        room_id = validated_data.pop('room_id', None)
        instructor_id = validated_data.pop('instructor_id', None)
        meeting_time_id = validated_data.pop('meeting_time_id', None)
        
        department = Department.objects.get(dept_name=department_id)
        section = Section.objects.create(department=department, **validated_data)
        
        if course_id:
            section.course = Course.objects.get(course_number=course_id)
        if room_id:
            section.room = Room.objects.get(r_number=room_id)
        if instructor_id:
            section.instructor = Instructor.objects.get(uid=instructor_id)
        if meeting_time_id:
            section.meeting_time = MeetingTime.objects.get(pid=meeting_time_id)
        
        section.save()
        return section
    
    def update(self, instance, validated_data):
        """Update an existing Section instance."""
        department_id = validated_data.pop('department_id', None)
        course_id = validated_data.pop('course_id', None)
        room_id = validated_data.pop('room_id', None)
        instructor_id = validated_data.pop('instructor_id', None)
        meeting_time_id = validated_data.pop('meeting_time_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if department_id:
            instance.department = Department.objects.get(dept_name=department_id)
        if course_id is not None:
            instance.course = Course.objects.get(course_number=course_id) if course_id else None
        if room_id is not None:
            instance.room = Room.objects.get(r_number=room_id) if room_id else None
        if instructor_id is not None:
            instance.instructor = Instructor.objects.get(uid=instructor_id) if instructor_id else None
        if meeting_time_id is not None:
            instance.meeting_time = MeetingTime.objects.get(pid=meeting_time_id) if meeting_time_id else None
        
        instance.save()
        return instance


class RoutineGenerationSerializer(serializers.Serializer):
    """Serializer for routine generation request."""
    strategy_type = serializers.ChoiceField(
        choices=['genetic_algorithm'],
        default='genetic_algorithm',
        required=False
    )
    population_size = serializers.IntegerField(default=9, required=False, min_value=1, max_value=100)
    max_generations = serializers.IntegerField(default=1000, required=False, min_value=1, max_value=10000)
    mutation_rate = serializers.FloatField(default=0.1, required=False, min_value=0.0, max_value=1.0)


class TimetableItemSerializer(serializers.Serializer):
    """Serializer for timetable item in response."""
    section_id = serializers.IntegerField()
    section = serializers.CharField()
    department = serializers.CharField()
    course_number = serializers.CharField()
    course_name = serializers.CharField()
    max_students = serializers.CharField()
    room_number = serializers.CharField(allow_null=True)
    room_capacity = serializers.IntegerField(allow_null=True)
    instructor_uid = serializers.CharField(allow_null=True)
    instructor_name = serializers.CharField(allow_null=True)
    meeting_time_id = serializers.CharField(allow_null=True)
    meeting_day = serializers.CharField(allow_null=True)
    meeting_time = serializers.CharField(allow_null=True)


class TimetableSerializer(serializers.Serializer):
    """Serializer for timetable response."""
    schedule = TimetableItemSerializer(many=True)
    fitness = serializers.FloatField()
    conflicts = serializers.IntegerField()
    generations = serializers.IntegerField()


class GenerationHistorySerializer(serializers.Serializer):
    """Serializer for generation history."""
    id = serializers.CharField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    fitness_score = serializers.FloatField(read_only=True)
    conflicts_count = serializers.IntegerField(read_only=True)
    generations_run = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    strategy_type = serializers.CharField(read_only=True)
    parameters = serializers.DictField(read_only=True)
    created_by = serializers.CharField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)


class CountsSerializer(serializers.Serializer):
    """Serializer for entity counts."""
    rooms = serializers.IntegerField()
    instructors = serializers.IntegerField()
    courses = serializers.IntegerField()
    departments = serializers.IntegerField()
    sections = serializers.IntegerField()
    meeting_times = serializers.IntegerField()
    total_seating_capacity = serializers.IntegerField()


class AssignmentsSerializer(serializers.Serializer):
    """Serializer for assignment statistics."""
    total_sections = serializers.IntegerField()
    assigned_sections = serializers.IntegerField()
    partially_assigned_sections = serializers.IntegerField()
    unassigned_sections = serializers.IntegerField()
    completion_percentage = serializers.FloatField()


class RoomUtilizationItemSerializer(serializers.Serializer):
    """Serializer for room utilization item."""
    sections = serializers.IntegerField()
    capacity = serializers.IntegerField()
    utilization_percentage = serializers.FloatField()


class UtilizationSerializer(serializers.Serializer):
    """Serializer for utilization metrics."""
    room_utilization = serializers.DictField(
        child=RoomUtilizationItemSerializer(),
        read_only=True
    )
    instructor_workload = serializers.DictField(
        child=serializers.IntegerField(),
        read_only=True
    )
    time_slot_distribution = serializers.DictField(
        child=serializers.IntegerField(),
        read_only=True
    )
    day_distribution = serializers.DictField(
        child=serializers.IntegerField(),
        read_only=True
    )


class ReadinessSerializer(serializers.Serializer):
    """Serializer for system readiness."""
    ready = serializers.BooleanField()
    missing_items = serializers.ListField(child=serializers.CharField())


class RecentGenerationSerializer(serializers.Serializer):
    """Serializer for recent generation item."""
    timestamp = serializers.CharField()
    fitness_score = serializers.FloatField()
    conflicts_count = serializers.IntegerField()
    generations_run = serializers.IntegerField()
    status = serializers.CharField()
    strategy_type = serializers.CharField()


class GenerationHistoryStatsSerializer(serializers.Serializer):
    """Serializer for generation history statistics."""
    total_generations = serializers.IntegerField()
    average_fitness = serializers.FloatField()
    best_fitness = serializers.FloatField()
    average_conflicts = serializers.FloatField()
    success_count = serializers.IntegerField()
    failed_count = serializers.IntegerField()
    recent_generations = RecentGenerationSerializer(many=True)


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    counts = CountsSerializer()
    assignments = AssignmentsSerializer()
    utilization = UtilizationSerializer()
    readiness = ReadinessSerializer()
    generation_history = GenerationHistoryStatsSerializer()


class DepartmentStatusSerializer(serializers.Serializer):
    """Serializer for department status."""
    total = serializers.IntegerField()
    fully_assigned = serializers.IntegerField()
    partially_assigned = serializers.IntegerField()
    unassigned = serializers.IntegerField()


class SectionStatusSerializer(serializers.Serializer):
    """Serializer for section status."""
    fully_assigned = serializers.IntegerField()
    partially_assigned = serializers.IntegerField()
    unassigned = serializers.IntegerField()
    by_department = serializers.DictField(
        child=DepartmentStatusSerializer(),
        read_only=True
    )

