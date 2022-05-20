from django.urls import path
from app.views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('resume/', ResumeView.as_view(), name='resume'),
]
