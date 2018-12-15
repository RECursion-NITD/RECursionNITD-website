from django import forms
from .models import *
from django.contrib.auth.models import User

class Questionform(forms.ModelForm):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibility=models.BooleanField(max_length=10,default=True)

    class Meta:
        model = Questions
        fields = ('title','description','visibility')