from django import forms
from .models import *
from django.contrib.auth.models import User

class Questionform(forms.ModelForm):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    visibility=models.BooleanField(max_length=10,default=True)
    tag=models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        model = Questions
        fields = ('title','description','visibility')


class Tagsform(forms.ModelForm):
    name=models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        model = Tags
        fields = ('name',)  

class Taggingform(forms.ModelForm):
    
    class Meta:
        model = Taggings
        fields = ('question','tag')                