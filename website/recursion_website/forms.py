from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import mimetypes
from .validators import *
from django.contrib.auth.forms import UserCreationForm


class Questionform(forms.ModelForm):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibility = models.BooleanField(max_length=10, default=True)

    class Meta:
        model = Questions
        fields = ('title', 'description', 'visibility')


class Tagsform(forms.ModelForm):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        model = Tags
        fields = ('name',)


class Taggingform(forms.ModelForm):
    class Meta:
        model = Taggings
        fields = ('question', 'tag')

class Answerform(forms.ModelForm):
    description = models.TextField()

    class Meta:
        model = Answers
        fields = ('description',)

class Commentform(forms.ModelForm):
    body = models.TextField()

    class Meta:
        model = Comments
        fields = ('body',)

class Comment_Answerform(forms.ModelForm):
    body = models.TextField()

    class Meta:
        model = Comments_Answers
        fields = ('body',)

class Profileform(forms.ModelForm):
    name = models.CharField(max_length=100)
    college = models.TextField(max_length=100)
    dept = models.IntegerField
    image_url = models.URLField
    nickname = models.TextField(max_length=100)

    def clean_image_url(self):
        url = self.cleaned_data['image_url'].lower()
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise forms.ValidationError(_("Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)"))
        return url

    class Meta:
        model = Profile
        fields = ('name', 'college', 'dept', 'image_url', 'nickname')




class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Mandatory')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )