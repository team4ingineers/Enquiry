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



from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Add this line for the name field
    abc_id = models.CharField(max_length=100)
    email = models.EmailField()
    annual_income = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    category_certificate = models.FileField(upload_to='category_certificates/', blank=True, null=True)
    disability = models.CharField(max_length=100, blank=True, null=True)
    disability_certificate = models.FileField(upload_to='disability_certificates/', blank=True, null=True)
    id_proof = models.FileField(upload_to='id_proofs/', blank=True, null=True)
    exam_name = models.CharField(max_length=100)
    exam_roll_number = models.CharField(max_length=100)
    exam_marks = models.IntegerField(blank=True, null=True)
    exam_certificate = models.FileField(upload_to='exam_certificates/', blank=True, null=True)
    annual_income_certificate = models.FileField(upload_to='annual_income_certificates/', blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.email  # Or any other string representation you prefer
