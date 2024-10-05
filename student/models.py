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



<<<<<<< HEAD
from django.db import models
from college.models import College
from django.contrib.auth.models import User

class CollegeHealthScore(models.Model):
    college = models.OneToOneField(College, on_delete=models.CASCADE)
    health_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Score can be 0.00 to 100.00
    number_of_agreements = models.PositiveIntegerField(default=0)
    number_of_disagreements = models.PositiveIntegerField(default=0)

    def update_health_score(self):
        # A simple algorithm to calculate the health score. This can be refined.
        total_feedback = self.number_of_agreements + self.number_of_disagreements
        if total_feedback > 0:
            self.health_score = (self.number_of_agreements / total_feedback) * 100
        else:
            self.health_score = 0.00
        self.save()

    def __str__(self):
        return f"{self.college.user.username} - Health Score: {self.health_score}"

class StudentFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    college_health_score = models.ForeignKey(CollegeHealthScore, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=10, choices=[('Agree', 'Agree'), ('Disagree', 'Disagree')])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.feedback_type == 'Agree':
            self.college_health_score.number_of_agreements += 1
        else:
            self.college_health_score.number_of_disagreements += 1

        self.college_health_score.update_health_score()
=======
class Meeting(models.Model):
    enquiry = models.ForeignKey('Enquiry', on_delete=models.CASCADE, related_name='meetings')
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Meeting for {self.enquiry} on {self.meeting_date} at {self.meeting_time}"
>>>>>>> 0c63b5542ab139f0365bbadcf5c556f072fb1f91
