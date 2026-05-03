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
from django.urls import reverse
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django_prometheus.models import ExportModelOperationsMixin


def content_file_name(instance, filename):
    ext = "png"
    filename = str(instance.user.username) + "." + str(ext)
    return os.path.join('images/', filename)


class Profile(ExportModelOperationsMixin('profile'), models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    role_choices = (
        ('1', 'Superuser'),
        ('2', 'Member'),
        ('3', 'User')
    )
    role = models.CharField(max_length=50, choices=role_choices, default='3')
    dept = models.CharField(max_length=70, blank=True, null=True)
    url_CodeChef = models.URLField(blank=True, null=True)
    url_Codeforces = models.URLField(blank=True, null=True)
    url_SPOJ = models.URLField(blank=True, null=True)
    url_HackerRank = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=content_file_name)
    email_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        previous_image_name = None
        if self.pk:
            previous = Profile.objects.filter(pk=self.pk).only('image').first()
            if previous and previous.image:
                previous_image_name = previous.image.name

        # Only process when a new image file is uploaded.
        if self.image and not getattr(self.image, '_committed', True):
            img = Image.open(self.image)
            img = img.convert('RGB')
            output = BytesIO()
            img = img.resize((100, 100))
            img.save(output, format='PNG', quality=100)
            output.seek(0)

            canonical_name = content_file_name(self, self.image.name or '')
            if default_storage.exists(canonical_name):
                default_storage.delete(canonical_name)

            self.image.save(canonical_name, ContentFile(output.getvalue()), save=False)

        super(Profile, self).save(*args, **kwargs)

        new_image_name = self.image.name if self.image else None
        if (
            previous_image_name
            and previous_image_name != new_image_name
            and default_storage.exists(previous_image_name)
        ):
            default_storage.delete(previous_image_name)

    def get_absolute_url(self):
        return reverse('user_profile_api:user_detail', kwargs={'username': self.user.username})

    class Meta:
        managed = True


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
