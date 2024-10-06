from django.contrib import admin
from .models import CollegeTour, StudentProfile, Enquiry, College, HealthScore, StudentFeedback, Student, Stage

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

# Register the College model
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'type')
    search_fields = ('user__username', 'location', 'type')
    list_filter = ('type', 'location')

# Register HealthScore model with custom admin configuration
@admin.register(HealthScore)
class HealthScoreAdmin(admin.ModelAdmin):
    list_display = ('college', 'health_score', 'number_of_agreements', 'number_of_disagreements')
    search_fields = ('college__user__username',)
    list_filter = ('health_score',)
    ordering = ('-health_score',)

# Register StudentFeedback model with custom admin configuration
@admin.register(StudentFeedback)
class StudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'college_health_score', 'feedback_type', 'created_at')
    search_fields = ('student__user__username', 'college_health_score__college__user__username')
    list_filter = ('feedback_type', 'created_at')
    ordering = ('-created_at',)

# Register the Student model with custom admin configuration
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    ordering = ('user',)

admin.site.register(Student, StudentAdmin)

# Register the Stage model with custom admin configuration
class StageAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_stage')
    search_fields = ('student__user__username',)
    list_filter = ('current_stage',)

admin.site.register(Stage, StageAdmin)
