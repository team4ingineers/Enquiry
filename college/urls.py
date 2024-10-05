from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', college_signup, name='student_signup'),
    path('college_dashboard', college_dashboard_view, name='college_dashboard_view'),
    path('upload_invitation/', upload_invitation, name='upload_invitation'),
    path('download-excel-template/', download_excel_template, name='download_excel_template'),
]