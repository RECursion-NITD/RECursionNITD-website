from django.db import models
from django.contrib.auth.models import User

# DONE
class Events(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # TODO
    # AUTOGEN DATE TIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __str__(self):
        return self.title
    class Meta:
        managed = True
        db_table = 'events'
        verbose_name_plural = 'Events' 
