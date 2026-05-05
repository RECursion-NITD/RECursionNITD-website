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
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django_prometheus.models import ExportModelOperationsMixin

import sys


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
        # Only resize/re-encode when a BRAND NEW image is being uploaded.
        # InMemoryUploadedFile = file uploaded via a form (small, held in RAM).
        # TemporaryUploadedFile = file uploaded via a form (large, spooled to /tmp).
        # An existing ImageFieldFile (already on disk) must NOT be re-processed — that
        # was the root cause of all the _XXXXXXX suffix duplicates.
        is_new_upload = isinstance(self.image, (InMemoryUploadedFile, TemporaryUploadedFile))

        if self.image and is_new_upload:
            # Step 1: Delete the old image file from disk before writing the new one.
            # This prevents Django from appending a random suffix because it found an
            # existing file at the same target path.
            try:
                old = Profile.objects.get(pk=self.pk)
                if old.image:
                    storage = old.image.storage
                    if storage.exists(old.image.name):
                        storage.delete(old.image.name)
            except Profile.DoesNotExist:
                pass  # Brand-new profile — no old image to clean up.

            # Step 2: Resize the new upload to 100x100 pixels.
            img = Image.open(self.image)
            output = BytesIO()
            img = img.resize((100, 100))
            img.save(output, format='PNG', quality=100)
            output.seek(0)

            # Step 3: Wrap the resized bytes in an InMemoryUploadedFile.
            # Pass the STABLE filename (username.png) so content_file_name returns
            # images/username.png — and since we just deleted that file, Django will
            # write it cleanly with NO random suffix.
            self.image = InMemoryUploadedFile(
                output, 'ImageField', f"{self.user.username}.png",
                'image/png', sys.getsizeof(output), None
            )

        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile_api:user_detail', kwargs={'username': self.user.username})

    class Meta:
        managed = True


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        # A new User was just registered — create their Profile.
        # Profile.objects.create() already calls save() internally, so we stop here.
        Profile.objects.create(user=instance)
    else:
        # An existing User was updated (password reset, email confirm, admin edit, etc.).
        # We still need to save the profile to persist any in-memory field changes
        # (e.g. profile.email_confirmed = True set before user.save() was called).
        # This is now SAFE because Profile.save() only re-processes genuinely new uploads.
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # Edge case: user exists but has no profile yet — create one.
            Profile.objects.create(user=instance)
