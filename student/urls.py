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
    path('airecommendation/', airecommendation, name = 'airecommendation')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)