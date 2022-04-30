from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import os

def content_file_name(instance,filename):
	ext="png"
	filename= str(instance.title)+"."+str(ext)
	return os.path.join('images/',filename)

class Events_Calendar(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_choices = (
        ('Class', 'Class'),
        ('Contest', 'Contest'),
        ('Event', 'Event'),
    )
    year_choices = (
        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('First and Second Year', 'First and Second Year'),
        ('NIT Durgapur', 'NIT Durgapur'),
        ('Global Participants', 'Global Participants'),
    )
    event_type = models.CharField(max_length=20, choices=event_choices ,default='Class')
    target_year = models.CharField(max_length=40, choices=year_choices ,default='First Year')
    description = MarkdownxField(null=True,blank=True)
    image = models.ImageField(blank=True, null=True, upload_to=content_file_name)
    link = models.URLField(null=True,blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.CharField(max_length=20, null=True, blank=True)
    venue = models.CharField(max_length=20,default="Online",null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.description)
    
    def __str__(self):
        return self.event_type + " - " + self.title
    class Meta:
        managed = True
        db_table = 'events_calendar'
        verbose_name_plural = 'Events_Calendar'
