from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import mimetypes
from .validators import *
from django.contrib.auth.forms import UserCreationForm

class Profileform(forms.ModelForm):
    name = models.CharField(max_length=100)
    college = models.TextField(max_length=100)
    dept = models.IntegerField()
    url_CodeChef = models.URLField()
    url_Codeforces = models.URLField()
    url_SPOJ = models.URLField()
    url_HackerRank = models.URLField()

    def clean_image_url(self):
        url = self.cleaned_data['image_url'].lower()
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise forms.ValidationError(_("Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"))
        return url

    class Meta:
        model = Profile
        fields = ('name', 'college', 'dept', 'image', 'url_CodeChef', 'url_Codeforces', 'url_SPOJ', 'url_HackerRank',)




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Mandatory')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if is_disposable_email(email):
            raise forms.ValidationError(_("Temporary or disposable email addresses are not allowed. Please use a permanent email address."))
        return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class EmailForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Mandatory')

    class Meta:
        model = User
        fields = ('email',)
