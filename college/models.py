from django.contrib.auth.models import User
from django.db import models

from django.db import models
from django.contrib.auth.models import User

class College(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking college to a user (admin/representative)
    established_year = models.PositiveIntegerField()
    type = models.CharField(max_length=50, choices=[('Public', 'Public'), ('Private', 'Private')])
    location = models.CharField(max_length=255)
    campus_area = models.DecimalField(max_digits=6, decimal_places=2)  # In acres
    established_by = models.CharField(max_length=255)
    nirf_ranking = models.PositiveIntegerField()
    total_departments = models.PositiveIntegerField()
    admission_criteria = models.CharField(max_length=255)
    top_courses = models.CharField(max_length=255)  # You can modify this to ManyToMany if needed
    official_website = models.URLField()

    def __str__(self):
        return self.user.username  # Returns the username of the user linked to the college
