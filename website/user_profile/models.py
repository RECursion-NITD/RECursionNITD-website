# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    role_choices = (
        ('1', 'Superuser'),
        ('2', 'Member'),
        ('3', 'User')
    )
    role = models.CharField(max_length=50, choices=role_choices ,default='3')
    dept = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    nickname = models.CharField(max_length=100, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __self__(self):
        return self.name

    class Meta:
        managed = True

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()