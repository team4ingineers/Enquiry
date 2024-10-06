from django.contrib import admin
from .models import CollegeTour, StudentProfile, Enquiry

# Register CollegeTour model
admin.site.register(CollegeTour)

# Register StudentProfile model with custom admin configuration
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'abc_id', 'email', 'annual_income', 'category', 'disability')
    search_fields = ('name', 'abc_id', 'email')
    list_filter = ('annual_income', 'category', 'disability')
    ordering = ('name',)

# Register Enquiry model
admin.site.register(Enquiry)


from django.contrib import admin
from .models import CollegeHealthScore, StudentFeedback

admin.site.register(CollegeHealthScore)
admin.site.register(StudentFeedback)

from django.contrib import admin
from .models import Student, Stage

# Register the Student model
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  # Display these fields in the admin list view

admin.site.register(Student, StudentAdmin)

# Register the Stage model
class StageAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_stage')  # Display these fields in the admin list view

admin.site.register(Stage, StageAdmin)
