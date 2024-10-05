from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def college_signup(request):
    if request.method == 'POST':
        form = CollegeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and automatically assign to Mentor group
            mentor_group = Group.objects.get_or_create(name='MENTOR')
            mentor_group[0].user_set.add(user)
            login(request, user)  # Log in the new user
            return redirect('college_dashboard_view')
    else:
        form = CollegeSignUpForm()

    return render(request, 'college_signup.html', {'form': form})


@login_required
def college_dashboard_view(request):
    return render(request, 'college_dashboard.html', {'user_type': 'College'})


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

def upload_invitation(request):
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
    return render(request, 'upload_invitation.html')






from django.http import FileResponse
from django.conf import settings
import os

def download_excel_template(request):
    # Path to the Excel template in the static directory
    file_path = os.path.join(settings.BASE_DIR, 'static','CSS', 'standard_template.xlsx')  # Adjust the path as necessary

    # Serve the file for download
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='standard_template.xlsx')
