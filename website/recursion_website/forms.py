from django import forms
from .models import *
from django.contrib.auth.models import User


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

class Profileform(forms.ModelForm):
    name = models.CharField(max_length=100)
    email = models.TextField(max_length=50)
    college = models.TextField(max_length=100)
    role = models.IntegerField
    dept = models.IntegerField
    image_url = models.URLField
    nickname = models.TextField(max_length=100)

    class Meta:
        model = Profile
        fields = ('name', 'email', 'college', 'role', 'dept', 'image_url', 'nickname')
