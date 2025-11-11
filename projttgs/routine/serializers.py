"""
DRF serializers for routine app.
Following DTO Pattern - separate domain models from API representation.
"""
from rest_framework import serializers
from routine.models import (
    Room, Instructor, MeetingTime, Course, Department, Section
)


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model."""
    
    class Meta:
        model = Room
        fields = ['id', 'r_number', 'seating_capacity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InstructorSerializer(serializers.ModelSerializer):
    """Serializer for Instructor model."""
    
    class Meta:
        model = Instructor
        fields = ['id', 'uid', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MeetingTimeSerializer(serializers.ModelSerializer):
    """Serializer for MeetingTime model."""
    
    class Meta:
        model = MeetingTime
        fields = ['pid', 'time', 'day', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    instructors = InstructorSerializer(many=True, read_only=True)
    instructor_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Instructor.objects.all(),
        source='instructors',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Course
        fields = [
            'course_number', 'course_name', 'max_numb_students',
            'instructors', 'instructor_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""
    courses = CourseSerializer(many=True, read_only=True)
    course_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        source='courses',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Department
        fields = ['id', 'dept_name', 'courses', 'course_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for Section model."""
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True,
        required=False,
        allow_null=True
    )
    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True,
        required=False,
        allow_null=True
    )
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(),
        source='instructor',
        write_only=True,
        required=False,
        allow_null=True
    )
    meeting_time = MeetingTimeSerializer(read_only=True)
    meeting_time_id = serializers.PrimaryKeyRelatedField(
        queryset=MeetingTime.objects.all(),
        source='meeting_time',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Section
        fields = [
            'section_id', 'department', 'department_id', 'num_class_in_week',
            'course', 'course_id', 'room', 'room_id', 'instructor', 'instructor_id',
            'meeting_time', 'meeting_time_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


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

