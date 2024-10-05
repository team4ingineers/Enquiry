from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('student_dashboard', student_dashboard_view, name='student_dashboard_view'),
    path('tour/<int:id>/', college_tour, name='college_tour'),
    path('events/category/google_drive/', upload_photo, name='upload_photo'),
    path('events/category/google_drive/folder/<str:folder_id>/', view_folder_contents, name='view_folder_contents'),
]