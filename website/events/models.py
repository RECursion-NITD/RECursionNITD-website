from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# DONE
class Events(models.Model):
    title = models.CharField(max_length=30)
    description = MarkdownxField()
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # TODO
    # AUTOGEN DATE TIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.description)

    def __str__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'events'
        verbose_name_plural = 'Events' 
