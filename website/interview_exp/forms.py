from django import forms
from .models import *
from django.contrib.auth.models import User
from markdownx.fields import MarkdownxFormField

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experiences
        interview_Questions = MarkdownxFormField()
        fields = ['company', 'year', 'job_Profile', 'role_Type', 'no_of_Rounds', 'interview_Questions', 'total_Compensation']

class SearchForm(forms.Form):
    key = forms.CharField(max_length=25)

class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revisions
        fields = ['message',]
