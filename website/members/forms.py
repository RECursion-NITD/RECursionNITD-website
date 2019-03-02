from django import forms
from . import models

class CreateMember(forms.ModelForm):
	class Meta:
		model = models.Members
		fields=['name','year_of_graduation','position','branch','contact_details','experience','profile_picture']
		
