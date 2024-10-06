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


from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import College
from django.urls import reverse

class CollegeLoginView(LoginView):
    template_name = 'college_login.html'

    def get_success_url(self):
        # Redirect to college dashboard after successful login
        return reverse('college_dashboard')

@login_required
def college_dashboard_view(request):
    college = College.objects.get(user=request.user)
    enquiries = college.enquiry_set.all()  # Retrieve all enquiries made for this college
    enquiries.update(seen_by_college=True)  # Mark them as seen
    return render(request, 'college_dashboard.html', {'enquiries': enquiries, 'user_type': 'College'})



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

    return render(request, 'update_enquiry.html', {'enquiry': enquiry})



import os
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.utils.html import strip_tags


from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import os

from django.contrib import messages

from django.contrib import messages

def upload_mail(request):
    if request.method == 'POST':
        # File upload
        excel_file = request.FILES.get('excel_file')
        email_subject = request.POST.get('email_subject')
        email_body_template = request.POST.get('email_body')

        if not excel_file or not email_subject or not email_body_template:
            return HttpResponse("Please upload all required fields and provide email content.")

        # Save uploaded Excel file
        fs = FileSystemStorage()
        excel_path = fs.save(excel_file.name, excel_file)

        # Read the Excel file
        try:
            df = pd.read_excel(
                os.path.join(settings.MEDIA_ROOT, excel_path),
                sheet_name="Guests",  # Update sheet name if needed
                na_values=""
            )
        except Exception as e:
            return HttpResponse(f"Error reading Excel file: {e}")

        # Track if all emails were sent successfully
        all_emails_sent = True

        # Save uploaded invitation files (if any)
        invitation_files = request.FILES.getlist('invitation_files')

        # Send email to each student
        for _, row in df.iterrows():
            try:
                student_name = row['Student Name']
                student_email = row['Student Email ID']
                student_phone = row['Student Phone No']

                # Convert student_phone to string
                student_phone_str = str(student_phone)

                # Replace placeholders in email body
                email_body = email_body_template.replace('{{student_name}}', student_name).replace('{{student_phone}}', student_phone_str)

                # HTML email content
                html_body = f"""
                <html>
                <body>
                    <p>{email_body}</p>

                    <br>

                    <p>Best Regards,<br>
                    <strong>The Event Team</strong></p>
                </body>
                </html>
                """

                # Create the email message
                email = EmailMessage(
                    email_subject,
                    html_body,
                    settings.DEFAULT_FROM_EMAIL,  # Use a default email from settings
                    [student_email],
                )
                email.content_subtype = 'html'  # Set the email content type to HTML

                # Attach invitation files if any
                for invitation_file in invitation_files:
                    email.attach(invitation_file.name, invitation_file.read(), invitation_file.content_type)

                # Send the email
                email.send()
                print(f"Invitation sent to {student_email}")
            except Exception as e:
                print(f"Failed to send email to {student_email}: {e}")
                all_emails_sent = False  # Set the flag to False if any email fails

        # Add a success message only if all emails were sent successfully
        if all_emails_sent:
            messages.success(request, "Mails sent successfully!")
        else:
            messages.error(request, "Some mails failed to send. Please check the logs.")

    # Render the upload invitations template
    return render(request, 'mail.html')






from django.http import FileResponse
from django.conf import settings
import os

def download_excel_template(request):
    # Path to the Excel template in the static directory
    file_path = os.path.join(settings.BASE_DIR, 'static','CSS', 'standard_template.xlsx')  # Adjust the path as necessary

    # Serve the file for download
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='standard_template.xlsx')


from django.shortcuts import render
from student.models import Meeting

def college_meetings(request):
    # Get the logged-in college
    college = request.user.college

    # Fetch all meetings where the enquiry is associated with this college
    meetings = Meeting.objects.filter(enquiry__college=college).order_by('meeting_date', 'meeting_time')

    return render(request, 'college_meetings.html', {'meetings': meetings})


from django.shortcuts import render, get_object_or_404, redirect
from student.models import Meeting
from student.forms import UpdateMeetingStatusForm

def update_meeting_status(request, id):
    meeting = get_object_or_404(Meeting, id=id)

    if request.method == 'POST':
        form = UpdateMeetingStatusForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('college_meetings')  # Redirect to the meetings list after updating
    else:
        form = UpdateMeetingStatusForm(instance=meeting)

    return render(request, 'update_meeting_status.html', {'form': form, 'meeting': meeting})


from django.shortcuts import render
from student.models import Enquiry

def college_students_enquired(request):
    # Get the logged-in college
    college = request.user.college

    # Fetch all enquiries for this college
    enquiries = Enquiry.objects.filter(college=college).select_related('student')

    # Get the list of unique students who have enquired
    students = {enquiry.student for enquiry in enquiries}

    return render(request, 'college_students_enquired.html', {'students': students})


def college_student_enquiries(request, student_id):
    college = request.user.college
    enquiries = Enquiry.objects.filter(college=college, student_id=student_id)

    return render(request, 'college_student_enquiries.html', {'enquiries': enquiries})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import College

@login_required
def college_enquiries_view(request):
    college = College.objects.get(user=request.user)
    enquiries = college.enquiry_set.all()  # Retrieve all enquiries for this college
    enquiries.update(seen_by_college=True)  # Mark all as seen when the page is accessed
    return render(request, 'college_enquiries.html', {'enquiries': enquiries})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from student.models import Enquiry, Meeting
from .forms import MeetingForm

@login_required
def schedule_meeting_view(request, enquiry_id):
    enquiry = get_object_or_404(Enquiry, id=enquiry_id)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.enquiry = enquiry  # Associate with the enquiry
            meeting.save()
            return redirect('schedule_meeting', enquiry_id=enquiry.id)
    else:
        form = MeetingForm()

    meetings = Meeting.objects.filter(enquiry=enquiry).order_by('meeting_date', 'meeting_time')

    return render(request, 'schedule_meeting.html', {
        'form': form,
        'enquiry': enquiry,
        'meetings': meetings,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from student.models import Enquiry, Meeting
from .forms import MeetingForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from student.models import Meeting, Enquiry
from .forms import MeetingForm
from django.http import JsonResponse

@login_required
def update_meeting_view(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('college_meetings')
    else:
        form = MeetingForm(instance=meeting)

    # Fetch meetings related to the enquiry to display them
    meetings = Meeting.objects.filter(enquiry__college=meeting.enquiry.college)

    return render(request, 'update_meeting.html', {
        'form': form,
        'meetings': meetings,  # Pass meetings for the calendar
    })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Meeting

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Meeting

@login_required
def approved_rescheduled_meetings_view(request):
    # Fetch all approved and rescheduled meetings for the logged-in user's college
    meetings = Meeting.objects.filter(
        enquiry__college=request.user.college,
        status__in=['APPROVED', 'RESCHEDULED']
    )

    return render(request, 'approved_rescheduled_meetings.html', {
        'meetings': meetings,
    })

def scholarshipai(request):
    return render(request, 'scholarshipai.html')

import os
from dotenv import load_dotenv
import google.generativeai as genai
from django.shortcuts import render

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Generation configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

def scholarshipai(request):
    # Initialize the formatted response to avoid UnboundLocalError
    formatted_response = "No results yet. Please fill out the form and search for scholarships."

    if request.method == "POST":
        name = request.POST.get("name", "")
        age = request.POST.get("age", "")
        gender = request.POST.get("gender", "")
        category = request.POST.get("category", "")
        income = request.POST.get("income", "")
        pwd_status = request.POST.get("pwd_status", "")
        jk_minority = request.POST.get("jk_minority", "")
        field_of_study = request.POST.get("field_of_study", "")
        extra_info = request.POST.get("extra_info", "")

        user_input = (
            f"Suggest scholarships based on the following criteria:\n"
            f"Name: {name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Category: {category}\n"
            f"Annual Income: {income}\n"
            f"PWD Status: {pwd_status}\n"
            f"J&K Minority Status: {jk_minority}\n"
            f"Field of Study: {field_of_study}\n"
            f"Extra Information: {extra_info}\n"
            "Provide detailed information about the available scholarships."
        )

        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",
                generation_config=generation_config,
            )

            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(user_input)
            response_text = response.text

            # Format the response text for clean output
            formatted_response = format_response(response_text)

        except Exception as e:
            formatted_response = f"An error occurred: {str(e)}"

    context = {'response': formatted_response}
    return render(request, 'scholarshipai.html', context)

def format_response(response_text):
    # Break the response text into lines
    lines = response_text.split("\n")
    formatted_lines = []

    for line in lines:
        if line.strip():
            if line[0].isdigit():
                formatted_lines.append(f"<p><strong>{line}</strong></p>")
            else:
                formatted_lines.append(f"<p>{line}</p>")

    # Join the formatted lines back into a string
    return "\n".join(formatted_lines)



from django.shortcuts import render, get_object_or_404
from student.models import Student, Stage  # Import models from student app
from django.http import JsonResponse
import json

# Display students in various stages
def manage_students(request):
    enquired_students = Stage.objects.filter(current_stage='Enquired')
    admission_students = Stage.objects.filter(current_stage='Admission')
    counseling_students = Stage.objects.filter(current_stage='Counseling')

    context = {
        'enquired_students': enquired_students,
        'admission_students': admission_students,
        'counseling_students': counseling_students,
    }
    return render(request, 'manage_students.html', context)

# Handle AJAX request to update student's stage
def update_stage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        new_stage = data.get('new_stage').capitalize()

        student = get_object_or_404(Student, id=student_id)
        stage = get_object_or_404(Stage, student=student)
        
        # Update the student's stage
        stage.current_stage = new_stage
        stage.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)





from django.shortcuts import render
from student.models import Meeting
from django.utils import timezone
from django.db.models import Q

def meeting_list(request):
    # Get current date and time
    now = timezone.now()

    # Define upcoming meetings
    upcoming_meetings = Meeting.objects.filter(
        Q(meeting_date__gt=now.date()) |
        (Q(meeting_date=now.date()) & Q(meeting_time__gt=now.time()))
    ).order_by('meeting_date', 'meeting_time')

    # Fetch past meetings
    past_meetings = Meeting.objects.filter(
        Q(meeting_date__lt=now.date()) |
        (Q(meeting_date=now.date()) & Q(meeting_time__lt=now.time()))
    ).order_by('-meeting_date', '-meeting_time')

    context = {
        'upcoming_meetings': upcoming_meetings,
        'past_meetings': past_meetings,
    }
    
    return render(request, 'meeting_list.html', context)

from django.shortcuts import redirect

# View to start the meeting
def start_meeting(request):
    # Redirect back to the meetings list after starting the meeting
    return render(request,'video_chat.html')