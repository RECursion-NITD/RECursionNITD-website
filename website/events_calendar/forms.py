from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from markdownx.fields import MarkdownxFormField
import mimetypes
import pytz,datetime

class Eventsform(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )
    end_time = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M')
    )

    def clean_start_time(self):
        wrong_aware = self.cleaned_data['start_time']
        tz = pytz.timezone('Asia/Kolkata')
        dt = datetime.datetime.fromtimestamp(wrong_aware.timestamp())
        final_dt = tz.localize(dt)
        return final_dt

    def clean_end_time(self):
        wrong_aware=self.cleaned_data['end_time']
        tz=pytz.timezone('Asia/Kolkata')
        dt=datetime.datetime.fromtimestamp(wrong_aware.timestamp())
        final_dt=tz.localize(dt)
        return final_dt

    def clean_description(self):
        data = self.cleaned_data['description']
        data = markdownify(data)
        return data
    
    def clean(self):
        cd = self.cleaned_data
        if cd.get('end_time') and cd.get('start_time'):
            if cd.get('end_time') < cd.get('start_time'):
                self.add_error('end_time', "End Time should be Greater than Start Time !")
        return cd
        
    class Meta:
        model=Events_Calendar
        fields=('title','event_type','target_year','link','venue','description','image','start_time','end_time')

class SearchForm(forms.Form):
    q = forms.CharField(max_length=25)
