from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication & Navigation
    path('', views.landing_page, name='landing'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Job Applications CRUD
    path('applications/', views.application_list_view, name='application_list'),
    path('applications/add/', views.application_create_view, name='application_create'),
    path('applications/<int:pk>/', views.application_detail_view, name='application_detail'),
    path('applications/<int:pk>/edit/', views.application_update_view, name='application_update'),
    path('applications/<int:pk>/delete/', views.application_delete_view, name='application_delete'),

    # REST API
    path('api/applications/', views.JobApplicationListCreateAPIView.as_view(), name='api_application_list'),
    path('api/applications/<int:pk>/', views.JobApplicationDetailAPIView.as_view(), name='api_application_detail'),
]
