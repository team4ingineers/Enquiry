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










