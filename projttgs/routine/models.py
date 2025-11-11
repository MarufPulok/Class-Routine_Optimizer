"""
Routine generation models using mongoengine.
Following Single Responsibility Principle - models contain only data structure.
"""
from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime

# Constants
TIME_SLOTS = (
    ('9:00 - 10:00', '9:00 - 10:00'),
    ('10:00 - 11:00', '10:00 - 11:00'),
    ('11:00 - 12:00', '11:00 - 12:00'),
    ('12:00 - 1:00', '12:00 - 1:00'),
    ('2:00 - 3:00', '2:00 - 3:00'),
    ('3:00 - 4:00', '3:00 - 4:00'),
    ('4:00 - 5:00', '4:00 - 5:00'),
)

DAYS_OF_WEEK = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
)


class Room(Document):
    """Room model for class scheduling."""
    r_number = fields.StringField(max_length=6, unique=True, required=True)
    seating_capacity = fields.IntField(default=50)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_room',
        'indexes': ['r_number'],
        'ordering': ['r_number']
    }
    
    def __str__(self) -> str:
        return self.r_number


class Instructor(Document):
    """Instructor model for class scheduling."""
    uid = fields.StringField(max_length=6, unique=True, required=True)
    name = fields.StringField(max_length=25, required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_instructor',
        'indexes': ['uid'],
        'ordering': ['uid']
    }
    
    def __str__(self) -> str:
        return f'{self.uid} {self.name}'


class MeetingTime(Document):
    """Meeting time model for class scheduling."""
    pid = fields.StringField(max_length=5, primary_key=True, required=True)
    time = fields.StringField(max_length=50, choices=TIME_SLOTS, default='11:00 - 12:00')
    day = fields.StringField(max_length=15, choices=DAYS_OF_WEEK, required=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_meetingtime',
        'ordering': ['day', 'time']
    }
    
    def __str__(self) -> str:
        return f'{self.pid} {self.day} {self.time}'


class Course(Document):
    """Course model for class scheduling."""
    course_number = fields.StringField(max_length=8, primary_key=True, required=True)
    course_name = fields.StringField(max_length=40, required=True)
    max_numb_students = fields.StringField(max_length=65, required=True)
    instructors = fields.ListField(fields.ReferenceField('Instructor'), default=list)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_course',
        'ordering': ['course_number']
    }
    
    def __str__(self) -> str:
        return f'{self.course_number} {self.course_name}'


class Department(Document):
    """Department model for class scheduling."""
    dept_name = fields.StringField(max_length=50, unique=True, required=True)
    courses = fields.ListField(fields.ReferenceField('Course'), default=list)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_department',
        'indexes': ['dept_name'],
        'ordering': ['dept_name']
    }
    
    def get_courses(self):
        """Get all courses for this department."""
        return self.courses
    
    def __str__(self) -> str:
        return self.dept_name


class Section(Document):
    """Section model for class scheduling."""
    section_id = fields.StringField(max_length=25, primary_key=True, required=True)
    department = fields.ReferenceField('Department', required=True)
    num_class_in_week = fields.IntField(default=0)
    course = fields.ReferenceField('Course', null=True)
    meeting_time = fields.ReferenceField('MeetingTime', null=True)
    room = fields.ReferenceField('Room', null=True)
    instructor = fields.ReferenceField('Instructor', null=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'routine_section',
        'ordering': ['section_id']
    }
    
    def set_room(self, room: 'Room') -> None:
        """Set room for this section."""
        self.room = room
        self.save()
    
    def set_meetingTime(self, meeting_time: 'MeetingTime') -> None:
        """Set meeting time for this section."""
        self.meeting_time = meeting_time
        self.save()
    
    def set_instructor(self, instructor: 'Instructor') -> None:
        """Set instructor for this section."""
        self.instructor = instructor
        self.save()
    
    def __str__(self) -> str:
        return self.section_id
