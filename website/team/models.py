# This is an auto-generated Django model module.
import datetime
import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

def content_file_name(instance,filename):
	ext="png"
	filename= str(instance.name)+"."+str(ext)
	return os.path.join('images/',filename)

class Members(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    batch_year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2016), MaxValueValidator(2050)])
    url_Facebook = models.URLField()
    url_LinkedIn = models.URLField()
    mobile = models.CharField(max_length=13)
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