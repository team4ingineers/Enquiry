from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('send_enquiry/', send_enquiry, name='send_enquiry'),
    path('student_dashboard/', student_dashboard_view, name='student_dashboard'),
]