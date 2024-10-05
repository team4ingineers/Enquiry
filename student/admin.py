from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CollegeTour,Enquiry

# Register your models here
admin.site.register(CollegeTour)
admin.site.register(Enquiry)
