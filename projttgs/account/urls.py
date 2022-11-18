from django.urls import re_path, include
# from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    re_path('', include('django.contrib.auth.urls')),
    re_path('register/', views.register, name='register'),

    re_path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    re_path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    re_path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    re_path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done')
]


