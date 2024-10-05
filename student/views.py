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
            return redirect('student_dashboard_view')  # Redirect to the mentor's dashboard
    else:
        form = StudentSignUpForm()

    return render(request, 'student_signup.html', {'form': form})


@login_required
def student_dashboard_view(request):
    return render(request, 'student_dashboard.html', {'user_type': 'Student'})







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
            "1. IIT Bombay: Top-tier placements and great facilities.",
            "2. VJTI Mumbai: Excellent reviews with consistent placements.",
            "3. SPIT: Located in Andheri, good for engineering students."
        ]
    },
    {
        "marks_range": [85, 90],
        "location": "Mumbai",
        "course": "Engineering",
        "budget_range": [100000, 500000],
        "suggestions": [
            "1. KJ Somaiya: Excellent placements and strong faculty.",
            "2. DJ Sanghvi: Well-known for tech and engineering courses.",
            "3. Thadomal Shahani Engineering College: Affordable with great reviews."
        ]
    },
    # Additional colleges can be added here...
]

def get_college_recommendations(marks, location, course, budget):
    """ Fetch college recommendations from pre-defined college data. """
    for data in college_data:
        if data["marks_range"][0] <= marks <= data["marks_range"][1] and \
           "mumbai" in location.lower() and \
           data["course"].lower() == course.lower() and \
           data["budget_range"][0] <= budget <= data["budget_range"][1]:
            return "\n".join(data["suggestions"])
    return "No exact matches found. Try adjusting your filters."

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
            # Example: find the closest college based on lat/lon (pseudo-code)
            location = "Mumbai"  # Simulating for now

        # Fetch recommendations from pre-defined data
        college_suggestions = get_college_recommendations(marks, location, course, budget)
        
        if not college_suggestions:
            # Fallback to AI model if no pre-defined matches (optional)
            user_input = f"""
            Suggest engineering colleges in Mumbai for a student with:
            Name: {student_name}
            Marks: {marks}
            Address: {address}
            Location: {location}
            Course: {course}
            Budget: {budget}
            Special Requirements: {special_requirements}
            """

            model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            response_text = response.text
        else:
            response_text = college_suggestions

    context = {'response': response_text}
    return render(request, 'gemini.html', context)


from django.shortcuts import render
from .models import CollegeTour

def college_tour(request, tour_id):
    tour = CollegeTour.objects.get(id=tour_id)
    return render(request, 'college_tour.html', {'tour': tour})
