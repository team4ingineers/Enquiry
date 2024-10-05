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
