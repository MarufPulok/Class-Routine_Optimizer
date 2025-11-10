from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('^about/$', views.about, name='about'),
    re_path('^help/$', views.help, name='help'),
    re_path('^terms/$', views.terms, name='terms'),
    re_path('^contact/$', views.contact, name='contact'),

    re_path('admin_dashboard', views.admindash, name='admindash'),

    re_path('add_teachers', views.addInstructor, name='addInstructors'),
    re_path('teachers_list/', views.inst_list_view , name='editinstructor'),
    re_path('delete_teacher/<int:pk>/', views.delete_instructor, name='deleteinstructor'),

    re_path('add_rooms', views.addRooms, name='addRooms'),
    re_path('rooms_list/', views.room_list, name='editrooms'),
    re_path('delete_room/<int:pk>/', views.delete_room, name='deleteroom'),

    re_path('add_timings', views.addTimings, name='addTimings'),
    re_path('timings_list/', views.meeting_list_view, name='editmeetingtime'),
    re_path('delete_meetingtime/<str:pk>/', views.delete_meeting_time, name='deletemeetingtime'),

    re_path('add_courses', views.addCourses, name='addCourses'),
    re_path('courses_list/', views.course_list_view, name='editcourse'),
    re_path('delete_course/<str:pk>/', views.delete_course, name='deletecourse'),

    re_path('add_departments', views.addDepts, name='addDepts'),
    re_path('departments_list/', views.department_list, name='editdepartment'),
    re_path('delete_department/<int:pk>/', views.delete_department, name='deletedepartment'),

    re_path('add_sections', views.addSections, name='addSections'),
    re_path('sections_list/', views.section_list, name='editsection'),
    re_path('delete_section/<str:pk>/', views.delete_section, name='deletesection'),

    re_path('generate_timetable', views.generate, name='generate'),

    re_path('timetable_generation/', views.timetable, name='timetable'),
    re_path('timetable_generation/render/pdf', views.Pdf.as_view, name='pdf'),

]
