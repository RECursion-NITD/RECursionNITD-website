from django import forms
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import mimetypes



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

