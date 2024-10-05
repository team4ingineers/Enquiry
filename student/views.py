from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and automatically assign to Mentor group
            mentor_group = Group.objects.get_or_create(name='MENTOR')
            mentor_group[0].user_set.add(user)
            login(request, user)  # Log in the new user
            return redirect('student_dashboard')  # Redirect to the mentor's dashboard
    else:
        form = StudentSignUpForm()

    return render(request, 'student_signup.html', {'form': form})


@login_required
def send_enquiry(request):
    student = Student.objects.get(user=request.user)  # Get the logged-in student
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.student = student  # Associate the enquiry with the logged-in student
            enquiry.save()  # Save the enquiry to the database
            return redirect('student_dashboard')  # Redirect to student's dashboard after sending
    else:
        form = EnquiryForm()

    return render(request, 'student/send_enquiry.html', {'form': form})

@login_required
def student_dashboard_view(request):
    student = Student.objects.get(user=request.user)  # Get the logged-in student
    enquiries = Enquiry.objects.filter(student=student)  # Get all enquiries made by the student
    return render(request, 'student/student_dashboard.html', {'enquiries': enquiries, 'user_type': 'Student'})
