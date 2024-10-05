from django.db import models
from django.contrib.auth.models import User
from college.models import College

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Enquiry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    message = models.TextField()  # The enquiry message from the student
    date_created = models.DateTimeField(auto_now_add=True)  # Date the enquiry was made
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    seen_by_college = models.BooleanField(default=False)  # Tracks if college has seen the enquiry
    response = models.TextField(blank=True, null=True)  # College's response to the enquiry (optional)

    def __str__(self):
        return f"Enquiry from {self.student.user.username} to {self.college.user.username}"
        
        
        
class CollegeTour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/')

    def __str__(self):
        return self.name
