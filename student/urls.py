from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import * # Ensure these views are imported

urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('send_enquiry/', send_enquiry, name='send_enquiry'),
    path('student_dashboard/', student_dashboard_view, name='student_dashboard'),
    path('tour/<int:id>/', college_tour, name='college_tour'),
    # path('college-search/', college_search, name='college_search'),
    path('colleges/', colleges , name = 'colleges'),
    path('enquires/', enquires , name = 'enquires'),
    path('college-search/', college_search, name='college_search'),
    path('login/', StudentLoginView.as_view(), name='student_login'),
    path('student_dashboard', student_dashboard_view, name='student_dashboard_view'),
    path('tour/<int:id>/', college_tour, name='college_tour'),
    path('events/category/google_drive/', upload_photo, name='upload_photo'),
    path('events/category/google_drive/folder/<str:folder_id>/', view_folder_contents, name='view_folder_contents'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('studentactiveenquires/',studentactiveenquires, name='studentactiveenquires'),
    path('closedenquiry/',closedenquiry, name ='closedenquiry'),


    

    path('studentactiveenquires/',studentactiveenquires, name='studentactiveenquires'),
    path('closedenquiry/',closedenquiry, name ='closedenquiry'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('iitmadras/', iitmadras, name ='iitmadras'),
    path('enquiry/<int:id>/', enquiry_detail, name='enquiry_detail'),
    path('enquiry/<int:id>/schedule-meeting/', schedule_meeting, name='schedule_meeting'),
<<<<<<< HEAD
    
    path('health-scores/', health_score_list, name='health_score_list'),
    path('college/<int:college_id>/', college_health_details, name='college_health_details'),
    path('college/<int:college_id>/submit-feedback/', submit_feedback, name='submit_feedback'),
=======
    path('tools/',tools,name='tools'),
    path('college_tour/', college_tour, name='college_tour'),
>>>>>>> 782ff8cd15d73ead3391005301853eb81e0b9621
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)