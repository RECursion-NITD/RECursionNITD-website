from django import forms
from .models import *
from django.contrib.auth.models import User

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experiences
        fields = ['company', 'year', 'job_Profile', 'no_of_Rounds', 'interview_Questions', 'total_Compensation']