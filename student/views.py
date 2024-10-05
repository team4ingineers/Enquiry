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

    return render(request, 'send_enquiry.html', {'form': form})

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Student

from django.urls import reverse

class StudentLoginView(LoginView):
    template_name = 'student_login.html'

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
        try:
            marks = int(request.POST.get("marks", ""))
            budget = int(request.POST.get("budget", ""))
        except ValueError:
            return render(request, 'gemini.html', {'response': "Please enter valid numeric values for marks and budget."})

        address = request.POST.get("address", "")
        location = request.POST.get("location", "")
        course = request.POST.get("course", "")
        special_requirements = request.POST.get("special_requirements", "")

        # Process latitude, longitude if provided for current location
        if "," in location:
            try:
                lat, lon = map(float, location.split(","))
                location = "Mumbai"  # Simulating for now
            except ValueError:
                return render(request, 'gemini.html', {'response': "Invalid location format. Please use 'lat, lon'."})

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


def airecommendation(request):
    
    return render(request, 'gemini.html')


from django.shortcuts import render, get_object_or_404
from student.models import CollegeTour  # Import the CollegeTour model
from college.models import *

def college_tour(request, id):  # Ensure id is in the function definition
    tour = get_object_or_404(CollegeTour, id=id)
    return render(request, 'college_tour.html', {'tour': tour})


def colleges(request):
    all_colleges = College.objects.all()
    print(all_colleges)  # This will print the QuerySet in the console
    return render(request, 'colleges.html', {'colleges': all_colleges})


def enquires(request):
    student = Student.objects.get(user=request.user)
    enquiries = student.enquiry_set.all()  # Retrieve all enquiries made by the student
    return render(request, 'student_enquires.html', {'enquiries': enquiries, 'user_type': 'Student'})






from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.core.files.storage import FileSystemStorage
from googleapiclient.http import MediaFileUpload
import os
from googleapiclient.errors import HttpError


# Define your scopes and service account file
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'drive.json'
PARENT_FOLDER_ID = "1-znjTCTeW_Us22GqyvYMlys0AbDi-BMR"

# Function to authenticate user (service account for simplicity)
def authenticate_user():
    from google.oauth2.service_account import Credentials
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

# Function to create a new folder on Google Drive
def create_folder(folder_name, parent_folder_id=PARENT_FOLDER_ID):
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id] if parent_folder_id else None
    }

    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Folder '{folder_name}' created with ID: {folder.get('id')}")
        return folder.get('id')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

# Fetch folders from Google Drive
def list_folders():
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    # Retrieve folders, filtering by parent folder ID if necessary
    results = service.files().list(
        q=f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder'",
        fields="files(id, name)"
    ).execute()
    
    folders = results.get('files', [])
    
    return folders  # Return the folders list to be used in the template

# Upload a photo to the selected folder
def upload_photo_to_drive(file_path, file_name, folder_id):
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype='image/png')

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return file.get('id')

# View to handle both folder creation and file upload
def upload_photo(request):
    # Get the list of folders
    folders = list_folders()

    if request.method == 'POST':
        # Create a new folder
        if 'create_folder' in request.POST:
            folder_name = request.POST['folder_name']
            create_folder(folder_name)
            return redirect('upload_photo')  # Redirect to 'upload_photo'

        # Handle file uploads
        elif 'upload_file' in request.POST:
            selected_folder = request.POST['folder_id']
            uploaded_files = request.FILES.getlist('file')  # Get the list of uploaded files

            # Process each uploaded file
            for uploaded_file in uploaded_files:
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.path(filename)

                # Upload to Google Drive
                drive_file_id = upload_photo_to_drive(file_path, uploaded_file.name, selected_folder)

                # Optionally, delete the file after upload
                os.remove(file_path)

            return redirect('upload_photo')  # Redirect to 'upload_photo'

    # Render the upload_photo.html template, passing the folder list
    return render(request, 'upload_photo.html', {'folders': folders})



def view_folder_contents(request, folder_id):
    # Functionality to list files in the specified folder
    creds = authenticate_user()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()
    
    files = results.get('files', [])

    return render(request, 'folder_contents.html', {'files': files, 'folder_id': folder_id})




def complete_profile(request):
    return render(request,'profile_form.html')



from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import Enquiry

from django.shortcuts import redirect
from django.contrib import messages

@login_required
def complete_profile(request):
    student = request.user  # Assuming the user is a Student instance
    profile, created = StudentProfile.objects.get_or_create(student=student)  # Get or create profile

    # Check if the profile has already been completed
    if profile.is_completed:
        messages.info(request, 'Your profile has already been completed and cannot be edited again.')
        return HttpResponse('Completed')  # Replace 'profile_page' with the actual profile view name

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.student = student  # Set the student reference
            profile.is_completed = True  # Mark the profile as completed
            profile.save()  # Save the profile
            
            return HttpResponse('completetd')  # Replace 'profile_page' with the actual profile view name
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'complete_profile.html', {'form': form})





from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def student_dashboard_view(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        # Redirect the user to complete their profile if Student object doesn't exist
        return redirect('student_dashboard')
    
    # Your existing dashboard logic goes here
    return render(request, 'student_dashboard.html', {'student': student})
