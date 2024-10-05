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
<<<<<<< HEAD
admin.site.register(Enquiry)


from django.contrib import admin
from .models import CollegeHealthScore, StudentFeedback

admin.site.register(CollegeHealthScore)
admin.site.register(StudentFeedback)
=======
admin.site.register(Enquiry)
>>>>>>> 0c63b5542ab139f0365bbadcf5c556f072fb1f91
