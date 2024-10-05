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

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Student

from django.urls import reverse

class StudentLoginView(LoginView):
    template_name = 'student/student_login.html'

    def get_success_url(self):
        # Return the URL string using reverse
        return reverse('student_dashboard')


@login_required
def student_dashboard_view(request):
    student = Student.objects.get(user=request.user)
    enquiries = student.enquiry_set.all()  # Retrieve all enquiries made by the student
    return render(request, 'student_dashboard.html', {'enquiries': enquiries, 'user_type': 'Student'})








import os
from dotenv import load_dotenv
from django.shortcuts import render
import google.generativeai as genai

# Load the environment variables (for API keys)
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Predefined College Data for Engineering Colleges in Mumbai
college_data = [
    {
        "marks_range": [90, 100],
        "location": "Mumbai",
        "course": "Engineering",
        "budget_range": [100000, 500000],
        "suggestions": [
            {
                "name": "IIT Bombay",
                "details": "Top-tier placements and great facilities.",
                "address": "IIT Area, Powai, Mumbai.",
                "average_salary": "₹18 LPA",
                "courses_offered": ["B.Tech", "M.Tech", "PhD"]
            },
            {
                "name": "VJTI Mumbai",
                "details": "Excellent reviews with consistent placements.",
                "address": "Jawahar Nagar, Matunga, Mumbai.",
                "average_salary": "₹10 LPA",
                "courses_offered": ["B.Tech", "M.Tech"]
            },
            {
                "name": "SPIT",
                "details": "Located in Andheri, good for engineering students.",
                "address": "Andheri (W), Mumbai.",
                "average_salary": "₹8 LPA",
                "courses_offered": ["B.Tech", "M.Tech"]
            },
        ]
    },
    {
        "marks_range": [85, 90],
        "location": "Mumbai",
        "course": "Engineering",
        "budget_range": [100000, 500000],
        "suggestions": [
            {
                "name": "KJ Somaiya",
                "details": "Excellent placements and strong faculty.",
                "address": "Vidya Vihar, Mumbai.",
                "average_salary": "₹7 LPA",
                "courses_offered": ["B.Tech", "M.Tech"]
            },
            {
                "name": "DJ Sanghvi",
                "details": "Well-known for tech and engineering courses.",
                "address": "Vile Parle (W), Mumbai.",
                "average_salary": "₹9 LPA",
                "courses_offered": ["B.Tech"]
            },
            {
                "name": "Thadomal Shahani Engineering College",
                "details": "Affordable with great reviews.",
                "address": "Bandra (W), Mumbai.",
                "average_salary": "₹6 LPA",
                "courses_offered": ["B.Tech"]
            },
        ]
    },
    # Additional colleges can be added here...
]

def get_college_recommendations(marks, location, course, budget):
    """Fetch college recommendations from pre-defined college data."""
    recommendations = []
    for data in college_data:
        if (data["marks_range"][0] <= marks <= data["marks_range"][1] and
            "mumbai" in location.lower() and
            data["course"].lower() == course.lower() and
            data["budget_range"][0] <= budget <= data["budget_range"][1]):
            
            for suggestion in data["suggestions"]:
                recommendations.append(suggestion)
    
    return recommendations

def college_recommendation(request):
    response_text = ""
    if request.method == "POST":
        student_name = request.POST.get("student_name", "")
        marks = int(request.POST.get("marks", ""))
        address = request.POST.get("address", "")
        location = request.POST.get("location", "")
        course = request.POST.get("course", "")
        budget = int(request.POST.get("budget", ""))
        special_requirements = request.POST.get("special_requirements", "")

        # Process latitude, longitude if provided for current location
        if "," in location:
            lat, lon = map(float, location.split(","))
            location = "Mumbai"  # Simulating for now

        # Fetch recommendations from pre-defined data
        college_suggestions = get_college_recommendations(marks, location, course, budget)
        
        if not college_suggestions:
            # Fallback to AI model if no pre-defined matches
            user_input = f"""
            Suggest engineering colleges in Mumbai for a student with:
            Name: {student_name}
            Marks: {marks}
            Address: {address}
            Location: {location}
            Course: {course}
            Budget: {budget}
            Special Requirements: {special_requirements}

            Please provide a detailed response, including college names, addresses, courses offered, placement statistics, and any other relevant information.
            """

            model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            response_text = response.text
        else:
            # Prepare a detailed response from predefined suggestions
            response_text = "Here are some college suggestions based on your inputs:\n\n"
            for college in college_suggestions:
                response_text += f"**{college['name']}**\n"
                response_text += f"Details: {college['details']}\n"
                response_text += f"Address: {college['address']}\n"
                response_text += f"Average Salary: {college['average_salary']}\n"
                response_text += f"Courses Offered: {', '.join(college['courses_offered'])}\n\n"

    context = {'response': response_text}
    return render(request, 'gemini.html', context)



from django.shortcuts import render, get_object_or_404
from student.models import CollegeTour  # Import the CollegeTour model
from college.models import *

def college_tour(request, id):  # Ensure id is in the function definition
    tour = get_object_or_404(CollegeTour, id=id)
    return render(request, 'college_tour.html', {'tour': tour})


def colleges(request):
    all_colleges = College.objects.all()
    return render(request, 'colleges.html', {'colleges': all_colleges})


def enquires(request):
    student = Student.objects.get(user=request.user)
    enquiries = student.enquiry_set.all()  # Retrieve all enquiries made by the student
    return render(request, 'student/student_enquires.html', {'enquiries': enquiries, 'user_type': 'Student'})

def airecommendation(request):
    return render(request, 'gemini.html')
