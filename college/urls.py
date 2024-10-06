from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', college_signup, name='student_signup'),
    path('college_dashboard/', college_dashboard_view, name='college_dashboard'),
    path('enquiry/<int:enquiry_id>/update/', update_enquiry_status, name='update_enquiry_status'),
    path('login/', CollegeLoginView.as_view(), name='college_login'),
    path('mail/', upload_mail, name='mail'),
    path('download-excel-template/', download_excel_template, name='download_excel_template'),
    path('meetings/', college_meetings, name='college_meetings'),
    path('meetings/update/<int:id>/', update_meeting_status, name='update_meeting_status'),
    path('students-enquired/', college_students_enquired, name='college_students_enquired'),
    path('students-enquired/<int:student_id>/', college_student_enquiries, name='college_student_enquiries'),
    path('enquiries/', college_enquiries_view, name='college_enquiries'),
    path('schedule-meeting/<int:enquiry_id>/', schedule_meeting_view, name='schedule_meeting_view'),
    path('approved-rescheduled-meetings/', approved_rescheduled_meetings_view, name='approved_rescheduled_meetings'),
    path('analytics/',analytics, name='analytics'),
    path('scholarshipai/',scholarshipai,name ='scholarshipai'),
]