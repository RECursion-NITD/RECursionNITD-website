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
    email = models.EmailField(max_length=50)
    college = models.TextField(max_length=100)
    role = models.IntegerField
    dept = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)
    nickname = models.TextField(max_length=100)

    class Meta:
        model = Profile
        fields = ('name', 'email', 'college', 'role', 'dept', 'image_url', 'nickname')

class Eventsform(forms.ModelForm):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image_url = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 

    class Meta:
        model=Events
        fields=('title','description','image_url','start_time','end_time')
        
       
       

