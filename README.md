# 🎓 Class Routine Optimizer

A modern, intelligent timetable generation system built with Django, MongoDB, and Genetic Algorithms. Class Routine Optimizer helps educational institutions automatically generate optimal class schedules that satisfy both hard and soft constraints.

**Class Routine Optimizer** Django MongoDB Genetic Algorithm SQLite

## ✨ Features

### For Administrators

📚 **Data Management** - Comprehensive CRUD operations for all timetable components:

- 👨‍🏫 **Instructor Management** - Add, edit, and manage faculty members
- 🏫 **Room Management** - Manage classrooms with seating capacity tracking
- ⏰ **Meeting Time Management** - Configure available time slots and days
- 📖 **Course Management** - Create courses with instructor assignments and student capacity
- 🏛️ **Department Management** - Organize courses by departments
- 📋 **Section Management** - Manage class sections with course assignments

🧬 **Genetic Algorithm Optimization** - Advanced algorithm that:

- Satisfies hard constraints (no conflicts, room capacity, instructor availability)
- Optimizes soft constraints (preferred times, balanced schedules)
- Configurable population size and mutation rates
- Generates optimal timetables automatically

📊 **Timetable Generation** - Intelligent scheduling system:

- Automatic conflict detection and resolution
- Multi-constraint optimization
- Real-time generation progress
- Export to PDF format

📄 **PDF Export** - Download generated timetables as professional PDF documents

### Authentication & Security

🔐 **Django Authentication** - Secure user authentication system
🔒 **JWT Token Support** - RESTful API with JWT authentication
👤 **User Profiles** - Manage user profiles with additional information
🛡️ **Role-Based Access** - Secure admin dashboard access

### API Features

🌐 **RESTful API** - Complete REST API for all operations
📖 **API Documentation** - Interactive API docs with drf-spectacular (Swagger/ReDoc)
🔌 **CORS Support** - Configured for frontend integration
📝 **Serializers** - Comprehensive data validation and serialization

## 🛠️ Tech Stack

### Backend

- **Django 5.1** - Modern Python web framework
- **Django REST Framework** - Powerful REST API toolkit
- **MongoDB** - NoSQL database for flexible data storage (via mongoengine)
- **SQLite** - Relational database for Django's built-in features
- **mongoengine** - MongoDB ODM for Python
- **JWT Authentication** - Secure token-based authentication

### Services & Tools

- **drf-spectacular** - OpenAPI 3.0 schema generation
- **python-decouple** - Environment variable management
- **xhtml2pdf** - PDF generation from HTML templates
- **Pillow** - Image processing
- **django-cors-headers** - CORS handling for API

### Architecture

- **Repository Pattern** - Data access abstraction layer
- **Service Layer** - Business logic separation
- **Strategy Pattern** - Pluggable generation algorithms
- **Factory Pattern** - Dynamic strategy creation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (Python 3.13 recommended)
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/Class-Routine_Optimizer.git
cd Class-Routine_Optimizer
```

2. **Create and activate virtual environment**

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
cd projttgs
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the `projttgs` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Configuration
MONGODB_NAME=class_routine_db
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=
MONGODB_PASSWORD=
MONGODB_AUTH_SOURCE=admin

# CORS Settings (for frontend integration)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. **Set up the database**

```bash
# Run Django migrations (for SQLite)
python manage.py migrate

# MongoDB will be automatically connected when the server starts
```

6. **Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

8. **Open your browser**

Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 📁 Project Structure

```
Class-Routine_Optimizer/
├── projttgs/                    # Main project directory
│   ├── accounts/                # User authentication and profiles
│   │   ├── services/           # Authentication and user services
│   │   ├── repositories/       # Data access layer
│   │   └── serializers.py      # API serializers
│   │
│   ├── core/                    # Core utilities and base classes
│   │   ├── repositories/       # Base repository pattern
│   │   ├── services/           # Base service classes
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── routine/                 # Timetable generation app
│   │   ├── models.py           # MongoDB models (mongoengine)
│   │   ├── repositories/       # Data repositories
│   │   │   ├── course_repository.py
│   │   │   ├── department_repository.py
│   │   │   ├── instructor_repository.py
│   │   │   ├── meeting_time_repository.py
│   │   │   ├── room_repository.py
│   │   │   └── section_repository.py
│   │   ├── services/           # Business logic services
│   │   │   ├── routine_generation_service.py
│   │   │   ├── timetable_service.py
│   │   │   └── pdf_generation_service.py
│   │   ├── strategies/         # Generation algorithms
│   │   │   ├── base_strategy.py
│   │   │   └── genetic_algorithm_strategy.py
│   │   ├── factories/          # Factory pattern implementations
│   │   │   └── generation_factory.py
│   │   └── serializers.py      # API serializers
│   │
│   ├── projttgs/               # Django project settings
│   │   ├── settings.py         # Main configuration
│   │   ├── urls.py             # URL routing
│   │   └── wsgi.py             # WSGI configuration
│   │
│   ├── templates/              # HTML templates
│   ├── static/                 # Static files (CSS, JS, images)
│   ├── requirements.txt        # Python dependencies
│   └── manage.py               # Django management script
│
└── README.md                   # Project documentation
```

## 🎨 Key Features Implementation

### Genetic Algorithm Strategy

The timetable generation uses a sophisticated genetic algorithm that:

- **Population Initialization** - Creates diverse initial schedules
- **Fitness Evaluation** - Scores schedules based on constraint satisfaction
- **Selection** - Chooses best-performing schedules for reproduction
- **Crossover** - Combines features from parent schedules
- **Mutation** - Introduces random variations to explore solution space
- **Convergence** - Iteratively improves until optimal solution is found

### Repository Pattern

Data access is abstracted through repositories:

- **Separation of Concerns** - Business logic separated from data access
- **Testability** - Easy to mock and test
- **Flexibility** - Can switch data sources without changing business logic

### Service Layer Architecture

Business logic is encapsulated in service classes:

- **RoutineGenerationService** - Orchestrates timetable generation
- **TimetableService** - Manages timetable operations
- **PDFGenerationService** - Handles PDF export functionality

## 🔧 Available Scripts

```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Access Django shell with MongoDB models
python manage.py shell_plus
```

## 📝 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/)

## 🗄️ Database Schema

The application uses a hybrid database approach:

### MongoDB (via mongoengine)

- **Room** - Classroom information
- **Instructor** - Faculty members
- **MeetingTime** - Available time slots
- **Course** - Course details with instructor assignments
- **Department** - Academic departments
- **Section** - Class sections with course assignments

### SQLite (Django ORM)

- **User** - Django authentication users
- **Profile** - User profile information
- **Sessions** - Django session management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Maruf Hossain**

- GitHub: [@MarufPulok](https://github.com/MarufPulok)
- LinkedIn: [Maruf Hossain](https://www.linkedin.com/in/maruf-hossain)

## 🙏 Acknowledgments

- Built with Django and Django REST Framework
- Genetic algorithm implementation for constraint optimization
- MongoDB for flexible data storage
- UI components styled with Bootstrap
- PDF generation powered by xhtml2pdf

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

---

**Note**: This project uses both MongoDB (for timetable data) and SQLite (for Django's built-in features). Make sure MongoDB is running before starting the development server.
