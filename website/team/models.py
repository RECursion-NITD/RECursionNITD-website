# This is an auto-generated Django model module.
import datetime
import os
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

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

    def save(self, *args, **kwargs):
        # If a brand-new image is being uploaded, delete the old one from disk first.
        # This prevents Django from appending a random suffix (e.g. _XXXXXXX) to the
        # filename because the old file at that path already existed.
        if isinstance(self.image, (InMemoryUploadedFile, TemporaryUploadedFile)):
            try:
                old = Members.objects.get(pk=self.pk)
                if old.image:
                    storage = old.image.storage
                    if storage.exists(old.image.name):
                        storage.delete(old.image.name)
            except Members.DoesNotExist:
                pass  # New member record — no old image to remove.
        super(Members, self).save(*args, **kwargs)

    def get_cname(self):
        class_name = "Member"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'members'
        verbose_name_plural = 'Members'