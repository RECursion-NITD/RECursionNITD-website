# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import os
	
# Done
def content_file_name(instance,filename):
	ext=filename.split('.')[-1]
	filename="%s.%s" % (instance.id,ext)
	return os.path.join('profile_picture',filename)

class Members(models.Model):

	name = models.CharField(max_length=100)  
	year_of_graduation = models.CharField(max_length=20)  
	position = models.CharField(max_length=100)  
	branch = models.CharField(max_length=100)  
	contact_details = models.CharField(max_length=200) 
	experience = models.CharField(max_length=500)
	profile_picture=models.ImageField(upload_to=content_file_name, height_field=None, width_field=None, max_length=100,null=True)
	class Meta:
		managed = True
		db_table = 'members'
