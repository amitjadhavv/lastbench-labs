from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('staff/login/', views.StaffLoginView.as_view(), name='staff_login'),
    path('signup/', views.signup, name='signup'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('screening/start/', views.start_screening, name='start_screening'),
    path('screening/<int:session_id>/', views.screening_chat, name='screening_chat'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('candidate/<int:profile_id>/', views.candidate_detail, name='candidate_detail'),
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
