from django.contrib import admin
from .models import College

# @admin.register(College)
# class CollegeAdmin(admin.ModelAdmin):
#     list_display = (
#         'user', 
#         'type', 
#         'location', 
#         'campus_area', 
#         'established_by', 
#         'nirf_ranking', 
#         'total_departments', 
#         'admission_criteria', 
#         'top_courses', 
#         'official_website'
#     )
#     search_fields = ('user__username', 'location', 'type')

# Register other models if needed, but ensure College is not registered again
