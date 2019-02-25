from django import forms
from .models import *
from django.contrib.auth.models import User
from .validators import valid_url_extension
from .validators import valid_url_mimetype
from django.utils.translation import ugettext as _
import mimetypes

class Eventsform(forms.ModelForm):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image_url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 

    def clean_image_url(self):
        url = self.cleaned_data['image_url'].lower()
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise forms.ValidationError(_("Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"))
        return url

    class Meta:
        model=Events
        fields=('title','description','image_url','start_time','end_time')