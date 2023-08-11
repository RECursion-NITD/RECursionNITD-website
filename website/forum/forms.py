from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import mimetypes
from .validators import *
from django.contrib.auth.forms import UserCreationForm
from markdownx.fields import MarkdownxFormField
from markdownx.utils import markdownify

class Questionform(forms.ModelForm):
    title = models.CharField(max_length=100)
    description = MarkdownxFormField()
    anonymous_ask = models.BooleanField(max_length=10, default=False)

    def clean_description(self):
        data = self.cleaned_data['description']
        print(len(data)<20)
        if len(data)<20:
            raise forms.ValidationError("Description too Short! Less than 20 words!")
        data = markdownify(data)
        return data

    class Meta:
        model = Questions
        fields = ('title', 'description', 'anonymous_ask')


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
    description = MarkdownxFormField()

    def clean_description(self):
        data = self.cleaned_data['description']
        data = markdownify(data)
        return data


    class Meta:
        model = Answers
        fields = ('description',)

class Commentform(forms.ModelForm):
    body = MarkdownxFormField()

    def clean_body(self):
        data = self.cleaned_data['body']
        data = markdownify(data)
        return data

    class Meta:
        model = Comments
        fields = ('body',)

class Comment_Answerform(forms.ModelForm):
    body = MarkdownxFormField()

    def clean_body(self):
        data = self.cleaned_data['body']
        data = markdownify(data)
        return data

    class Meta:
        model = Comments_Answers
        fields = ('body',)

class SearchForm(forms.Form):
    key = forms.CharField(max_length=25)