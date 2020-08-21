from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='stats/login.html'),name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard')
]