from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

        class CollegeTour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/')

    def __str__(self):
        return self.name
