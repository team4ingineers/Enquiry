from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', college_signup, name='student_signup'),
    path('college_dashboard/', college_dashboard_view, name='college_dashboard'),
    path('enquiry/<int:enquiry_id>/update/', update_enquiry_status, name='update_enquiry_status'),
    path('login/', CollegeLoginView.as_view(), name='college_login'),
    path('mail/', upload_mail, name='mail'),
    path('download-excel-template/', download_excel_template, name='download_excel_template'),
]