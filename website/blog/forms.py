from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import mimetypes
from .validators import *
from django.contrib.auth.forms import UserCreationForm
from markdownx.fields import MarkdownxFormField
from markdownx.utils import markdownify

class Postform(forms.ModelForm):
    title = models.CharField(max_length=100)
    description = MarkdownxFormField()

    def clean_description(self):
        data = self.cleaned_data['description']
        if len(data)<20:
            raise forms.ValidationError("Description too Short! Less than 20 words!")
        data = markdownify(data)
        return data

    class Meta:
        model = Posts
        fields = ('title', 'description')


class Tagsform(forms.ModelForm):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        model = Tags
        fields = ('name',)


class Taggingform(forms.ModelForm):
    class Meta:
        model = Taggings
        fields = ('post', 'tag')

class Replyform(forms.ModelForm):
    description = MarkdownxFormField()

    def clean_description(self):
        data = self.cleaned_data['description']
        data = markdownify(data)
        return data


    class Meta:
        model = Reply
        fields = ('description',)

class Commentform(forms.ModelForm):
    body = MarkdownxFormField()

    def clean_body(self):
        data = self.cleaned_data['body']
        data = markdownify(data)
        return data

    class Meta:
        model = Comment
        fields = ('body',)

class Comment_Replyform(forms.ModelForm):
    body = MarkdownxFormField()

    def clean_body(self):
        data = self.cleaned_data['body']
        data = markdownify(data)
        return data

    class Meta:
        model = Comment_Reply
        fields = ('body',)

class SearchForm(forms.Form):
    key = forms.CharField(max_length=25)