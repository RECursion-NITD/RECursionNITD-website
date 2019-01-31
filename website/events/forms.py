from django import forms
from .models import *
from django.contrib.auth.models import User

class Eventsform(forms.ModelForm):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image_url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 

    class Meta:
        model=Events
        fields=('title','description','image_url','start_time','end_time')