from django.urls import path
from api.views import *

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    # Users
    path('users/', UsersView.as_view(), name='api_users'),
    # Resumes
    path('resumes/', ResumesView.as_view(), name='api_resumes'),
    path('resume/', ResumeView.as_view(), name='api_resume'),
]
