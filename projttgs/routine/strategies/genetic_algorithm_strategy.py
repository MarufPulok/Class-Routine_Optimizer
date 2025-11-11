"""
Genetic Algorithm strategy for routine generation.
Preserves the original genetic algorithm logic while following Strategy Pattern.
"""
import random as rnd
from typing import List, Dict, Any, Optional

from routine.models import Room, Instructor, MeetingTime, Course, Department, Section
from routine.strategies.base_strategy import BaseGenerationStrategy
from core.exceptions import RoutineGenerationError


# Genetic Algorithm Constants
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Class:
    """Represents a single class in a schedule."""
    
    def __init__(self, class_id: int, dept: Department, section: str, course: Course):
        self.section_id = class_id
        self.department = dept
        self.course = course
        self.instructor: Optional[Instructor] = None
        self.meeting_time: Optional[MeetingTime] = None
        self.room: Optional[Room] = None
        self.section = section

    def get_id(self) -> int:
        return self.section_id

    def get_dept(self) -> Department:
        return self.department

    def get_course(self) -> Course:
        return self.course

    def get_instructor(self) -> Optional[Instructor]:
        return self.instructor

    def get_meetingTime(self) -> Optional[MeetingTime]:
        return self.meeting_time

    def get_room(self) -> Optional[Room]:
        return self.room

    def set_instructor(self, instructor: Instructor) -> None:
        self.instructor = instructor

    def set_meetingTime(self, meeting_time: MeetingTime) -> None:
        self.meeting_time = meeting_time

    def set_room(self, room: Room) -> None:
        self.room = room


class Data:
    """Data container for all entities needed for schedule generation."""
    
    def __init__(self):
        self._rooms = list(Room.objects.all())
        self._meeting_times = list(MeetingTime.objects.all())
        self._instructors = list(Instructor.objects.all())
        self._courses = list(Course.objects.all())
        self._depts = list(Department.objects.all())

    def get_rooms(self) -> List[Room]:
        return self._rooms

    def get_instructors(self) -> List[Instructor]:
        return self._instructors

    def get_courses(self) -> List[Course]:
        return self._courses

    def get_depts(self) -> List[Department]:
        return self._depts

    def get_meetingTimes(self) -> List[MeetingTime]:
        return self._meeting_times


class Schedule:
    """Represents a single schedule solution."""
    
    def __init__(self, data: Data):
        self._data = data
        self._classes: List[Class] = []
        self._number_of_conflicts = 0
        self._fitness = -1
        self._class_numb = 0
        self._is_fitness_changed = True

    def get_classes(self) -> List[Class]:
        self._is_fitness_changed = True
        return self._classes

    def get_numb_of_conflicts(self) -> int:
        return self._number_of_conflicts

    def get_fitness(self) -> float:
        if self._is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False
        return self._fitness

    def initialize(self) -> 'Schedule':
        """Initialize schedule with random assignments."""
        sections = Section.objects.all()
        meeting_times = self._data.get_meetingTimes()
        rooms = self._data.get_rooms()
        
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            
            courses = list(dept.courses.all())
            if not courses:
                continue
            
            for course in courses:
                num_classes = n // len(courses) if len(courses) > 0 else n
                course_instructors = list(course.instructors.all())
                
                if not course_instructors:
                    continue
                
                for i in range(num_classes):
                    new_class = Class(self._class_numb, dept, section.section_id, course)
                    self._class_numb += 1
                    
                    # Random meeting time
                    if meeting_times:
                        new_class.set_meetingTime(
                            meeting_times[rnd.randrange(0, len(meeting_times))]
                        )
                    
                    # Random room
                    if rooms:
                        new_class.set_room(rooms[rnd.randrange(0, len(rooms))])
                    
                    # Random instructor
                    if course_instructors:
                        new_class.set_instructor(
                            course_instructors[rnd.randrange(0, len(course_instructors))]
                        )
                    
                    self._classes.append(new_class)
        
        return self

    def calculate_fitness(self) -> float:
        """Calculate fitness score (higher is better)."""
        self._number_of_conflicts = 0
        classes = self.get_classes()
        
        for i in range(len(classes)):
            # Check room capacity
            if classes[i].room and classes[i].course:
                try:
                    max_students = int(classes[i].course.max_numb_students)
                    if classes[i].room.seating_capacity < max_students:
                        self._number_of_conflicts += 1
                except (ValueError, TypeError):
                    pass
            
            # Check conflicts with other classes
            for j in range(i + 1, len(classes)):
                if (classes[i].meeting_time == classes[j].meeting_time and
                    classes[i].section_id != classes[j].section_id and
                    classes[i].section == classes[j].section):
                    
                    # Same room conflict
                    if classes[i].room == classes[j].room:
                        self._number_of_conflicts += 1
                    
                    # Same instructor conflict
                    if classes[i].instructor == classes[j].instructor:
                        self._number_of_conflicts += 1
        
        return 1 / (1.0 * self._number_of_conflicts + 1)


class Population:
    """Represents a population of schedules."""
    
    def __init__(self, size: int, data: Data):
        self._size = size
        self._data = data
        self._schedules = [Schedule(data).initialize() for _ in range(size)]

    def get_schedules(self) -> List[Schedule]:
        return self._schedules


class GeneticAlgorithm:
    """Genetic algorithm implementation for schedule evolution."""
    
    def __init__(self, population_size: int = POPULATION_SIZE,
                 num_elite: int = NUMB_OF_ELITE_SCHEDULES,
                 tournament_size: int = TOURNAMENT_SELECTION_SIZE,
                 mutation_rate: float = MUTATION_RATE):
        self.population_size = population_size
        self.num_elite = num_elite
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate

    def evolve(self, population: Population) -> Population:
        """Evolve population through crossover and mutation."""
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop: Population) -> Population:
        """Perform crossover operation on population."""
        data = pop._data
        crossover_pop = Population(0, data)
        
        # Keep elite schedules
        schedules = pop.get_schedules()
        schedules.sort(key=lambda x: x.get_fitness(), reverse=True)
        
        for i in range(self.num_elite):
            if i < len(schedules):
                crossover_pop.get_schedules().append(schedules[i])
        
        # Generate new schedules through crossover
        i = self.num_elite
        while i < self.population_size:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(
                self._crossover_schedule(schedule1, schedule2, data)
            )
            i += 1
        
        return crossover_pop

    def _mutate_population(self, population: Population) -> Population:
        """Perform mutation operation on population."""
        schedules = population.get_schedules()
        data = population._data
        
        for i in range(self.num_elite, len(schedules)):
            self._mutate_schedule(schedules[i], data)
        
        return population

    def _crossover_schedule(self, schedule1: Schedule, schedule2: Schedule, data: Data) -> Schedule:
        """Create new schedule by crossing over two parent schedules."""
        crossover_schedule = Schedule(data).initialize()
        classes1 = schedule1.get_classes()
        classes2 = schedule2.get_classes()
        crossover_classes = crossover_schedule.get_classes()
        
        for i in range(min(len(crossover_classes), len(classes1), len(classes2))):
            if rnd.random() > 0.5:
                crossover_classes[i] = classes1[i] if i < len(classes1) else crossover_classes[i]
            else:
                crossover_classes[i] = classes2[i] if i < len(classes2) else crossover_classes[i]
        
        return crossover_schedule

    def _mutate_schedule(self, mutate_schedule: Schedule, data: Data) -> Schedule:
        """Mutate a schedule by randomly changing some classes."""
        new_schedule = Schedule(data).initialize()
        mutate_classes = mutate_schedule.get_classes()
        new_classes = new_schedule.get_classes()
        
        for i in range(len(mutate_classes)):
            if self.mutation_rate > rnd.random():
                if i < len(new_classes):
                    mutate_classes[i] = new_classes[i]
        
        return mutate_schedule

    def _select_tournament_population(self, pop: Population) -> Population:
        """Select schedules using tournament selection."""
        data = pop._data
        tournament_pop = Population(0, data)
        schedules = pop.get_schedules()
        
        for _ in range(self.tournament_size):
            if schedules:
                tournament_pop.get_schedules().append(
                    schedules[rnd.randrange(0, len(schedules))]
                )
        
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class GeneticAlgorithmStrategy(BaseGenerationStrategy):
    """
    Genetic Algorithm strategy implementation.
    Following Strategy Pattern - can be swapped with other strategies.
    """
    
    def __init__(self, population_size: int = POPULATION_SIZE,
                 num_elite: int = NUMB_OF_ELITE_SCHEDULES,
                 tournament_size: int = TOURNAMENT_SELECTION_SIZE,
                 mutation_rate: float = MUTATION_RATE,
                 max_generations: int = 1000):
        self.population_size = population_size
        self.num_elite = num_elite
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
    
    def generate(self, **kwargs) -> Dict[str, Any]:
        """
        Generate routine using genetic algorithm.
        
        Returns:
            Dictionary with generated schedule data
        """
        try:
            data = Data()
            population = Population(self.population_size, data)
            genetic_algorithm = GeneticAlgorithm(
                population_size=self.population_size,
                num_elite=self.num_elite,
                tournament_size=self.tournament_size,
                mutation_rate=self.mutation_rate
            )
            
            generation_num = 0
            schedules = population.get_schedules()
            schedules.sort(key=lambda x: x.get_fitness(), reverse=True)
            
            # Evolve until perfect fitness or max generations
            while (generation_num < self.max_generations and
                   schedules[0].get_fitness() != 1.0):
                generation_num += 1
                population = genetic_algorithm.evolve(population)
                schedules = population.get_schedules()
                schedules.sort(key=lambda x: x.get_fitness(), reverse=True)
            
            best_schedule = schedules[0]
            classes = best_schedule.get_classes()
            
            # Convert to serializable format
            result = []
            for cls in classes:
                result.append({
                    'section_id': cls.section_id,
                    'section': cls.section,
                    'department': cls.department.dept_name,
                    'course_number': cls.course.course_number,
                    'course_name': cls.course.course_name,
                    'max_students': cls.course.max_numb_students,
                    'room_number': cls.room.r_number if cls.room else None,
                    'room_capacity': cls.room.seating_capacity if cls.room else None,
                    'instructor_uid': cls.instructor.uid if cls.instructor else None,
                    'instructor_name': cls.instructor.name if cls.instructor else None,
                    'meeting_time_id': cls.meeting_time.pid if cls.meeting_time else None,
                    'meeting_day': cls.meeting_time.day if cls.meeting_time else None,
                    'meeting_time': cls.meeting_time.time if cls.meeting_time else None,
                })
            
            return {
                'schedule': result,
                'fitness': best_schedule.get_fitness(),
                'conflicts': best_schedule.get_numb_of_conflicts(),
                'generations': generation_num,
            }
        except Exception as e:
            raise RoutineGenerationError(f"Error generating routine: {str(e)}")
    
    def get_fitness(self, schedule: Schedule) -> float:
        """Calculate fitness for a schedule."""
        return schedule.get_fitness()

