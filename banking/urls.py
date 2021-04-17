from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.TranscationView.as_view(), name='home'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('export/', views.ExportView.as_view(), name='export'),


]
