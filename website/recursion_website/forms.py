from django import forms
from . import models

class CreateMember(forms.ModelForm):
	class Meta:
		model = models.Members
		fields=['name','year','position','branch','contact_details','experience']
		
