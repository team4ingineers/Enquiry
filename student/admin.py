from django.contrib import admin

# Register your models here.
from django.contrib import admin
<<<<<<< HEAD
from .models import *

# Register your models here
admin.site.register(CollegeTour)
from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'abc_id', 'email', 'annual_income', 'category', 'disability')
    search_fields = ('name', 'abc_id', 'email')
    list_filter = ('annual_income', 'category', 'disability')
    ordering = ('name',)

# If you want to register more models, you can do it here as well.
=======
from .models import CollegeTour,Enquiry

# Register your models here
admin.site.register(CollegeTour)
admin.site.register(Enquiry)
>>>>>>> 5afd96a3ae01cb52ed7638cd32255edada1c6dc8
