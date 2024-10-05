from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('send_enquiry/', send_enquiry, name='send_enquiry'),
    path('student_dashboard/', student_dashboard_view, name='student_dashboard'),
    path('tour/<int:id>/', college_tour, name='college_tour'),
    path('aibot/', college_recommendation, name='college_recommendation'),
    path('colleges/', colleges , name = 'colleges'),
    path('enquires/', enquires , name = 'enquires'),
    path('airecommendation/', airecommendation, name = 'airecommendation'),
    path('login/', StudentLoginView.as_view(), name='student_login'),
    path('student_dashboard', student_dashboard_view, name='student_dashboard_view'),
    path('tour/<int:id>/', college_tour, name='college_tour'),
    path('events/category/google_drive/', upload_photo, name='upload_photo'),
    path('events/category/google_drive/folder/<str:folder_id>/', view_folder_contents, name='view_folder_contents'),
<<<<<<< HEAD
    path('complete-profile/', complete_profile, name='complete_profile'),
=======
    path('studentactiveenquires/',studentactiveenquires, name='studentactiveenquires'),
    path('closedenquiry/',closedenquiry, name ='closedenquiry'),
    
>>>>>>> 5afd96a3ae01cb52ed7638cd32255edada1c6dc8
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)