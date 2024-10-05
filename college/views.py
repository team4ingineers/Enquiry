from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from student.models import Enquiry

def college_signup(request):
    if request.method == 'POST':
        form = CollegeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and automatically assign to Mentor group
            mentor_group = Group.objects.get_or_create(name='MENTOR')
            mentor_group[0].user_set.add(user)
            login(request, user)  # Log in the new user
            return redirect('college_dashboard')
    else:
        form = CollegeSignUpForm()

    return render(request, 'college_signup.html', {'form': form})


@login_required
def college_dashboard_view(request):
    college = College.objects.get(user=request.user)  # Get the logged-in college
    enquiries = Enquiry.objects.filter(college=college)  # Get all enquiries for this college

    # Mark all enquiries as seen when the college views the dashboard
    enquiries.update(seen_by_college=True)

    return render(request, 'college/college_dashboard.html', {'enquiries': enquiries, 'user_type': 'College'})


@login_required
def update_enquiry_status(request, enquiry_id):
    enquiry = Enquiry.objects.get(id=enquiry_id, college__user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        response = request.POST.get('response')
        enquiry.status = status
        enquiry.response = response
        enquiry.save()
        return redirect('college_dashboard')

    return render(request, 'college/update_enquiry.html', {'enquiry': enquiry})
