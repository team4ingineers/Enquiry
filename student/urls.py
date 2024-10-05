from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('student_dashboard', student_dashboard_view, name='student_dashboard_view'),
     path('tour/<int:id>/', college_tour, name='college_tour'),
]