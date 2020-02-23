# This is an auto-generated Django model module.

import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

def content_file_name(instance,filename):
	ext="png"
	filename= str(instance.name)+"."+str(ext)
	return os.path.join('images/',filename)

class Members(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    batch_no = models.PositiveIntegerField(
        default= 1, validators=[MinValueValidator(1)])
    url_Facebook = models.URLField()
    url_LinkedIn = models.URLField()
    image = models.ImageField(upload_to=content_file_name)
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    def get_cname(self):
        class_name = "Member"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'members'
        verbose_name_plural = 'Members'