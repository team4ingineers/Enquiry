from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', college_signup, name='student_signup'),
    path('college_dashboard', college_dashboard_view, name='college_dashboard_view'),
]