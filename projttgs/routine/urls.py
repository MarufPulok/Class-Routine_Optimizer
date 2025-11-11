"""
URL configuration for routine app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from routine import views

app_name = 'routine'

# Create router for ViewSets
router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'instructors', views.InstructorViewSet, basename='instructor')
router.register(r'meeting-times', views.MeetingTimeViewSet, basename='meeting-time')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'sections', views.SectionViewSet, basename='section')

urlpatterns = [
    path('', include(router.urls)),
    path('generate/', views.RoutineGenerationView.as_view(), name='generate'),
    path('generate-pdf/', views.RoutinePDFGenerationView.as_view(), name='generate-pdf'),
]
