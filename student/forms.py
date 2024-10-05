from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user
    

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['college', 'message']  # Allow students to choose a college and write a message



from django import forms
from .models import StudentProfile

from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'name',
            'abc_id',
            'email',
            'annual_income',
            'category',
            'category_certificate',
            'disability',
            'disability_certificate',
            'id_proof',
            'exam_name',
            'exam_roll_number',
            'exam_marks',
            'exam_certificate',
            'annual_income_certificate',
            'additional_info'
        ]
        
    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        # You can customize your form fields here if needed.


from django import forms
from .models import Meeting

class ScheduleMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['meeting_date', 'meeting_time', 'description']
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'meeting_date': 'Meeting Date',
            'meeting_time': 'Meeting Time',
            'description': 'Description/Notes',
        }


from django import forms
from .models import Meeting

class UpdateMeetingStatusForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status', 'meeting_date', 'meeting_time']
        widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        
        # Ensure date and time are provided if rescheduling
        if status == 'RESCHEDULED':
            if not cleaned_data.get('meeting_date') or not cleaned_data.get('meeting_time'):
                raise forms.ValidationError("You must provide a new date and time when rescheduling.")
        return cleaned_data
