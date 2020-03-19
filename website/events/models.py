from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

# DONE
class Events(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    date = models.DateTimeField()
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

    def get_cname(self):  #Can be used to get the class name of the model
        class_name = "Event"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at'] #Will be arranged in order of 'created_at' attribute
        db_table = 'events'
        verbose_name_plural = 'Events'

    @property
    def get_html_url(self):
        url = reverse('events:event_detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
