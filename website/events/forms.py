from django import forms
from .models import *
from django.contrib.auth.models import User
from .validators import valid_url_extension
from .validators import valid_url_mimetype
from django.utils.translation import ugettext as _
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

    def clean_image_url(self):
        url = self.cleaned_data['image_url'].lower()
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise forms.ValidationError(_("Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"))
        return url

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

    class Meta:
        model=Events
        fields=('title','description','image_url','start_time','end_time')