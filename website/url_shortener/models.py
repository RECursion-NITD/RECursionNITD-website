from django.db import models
import string, random

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenedUrl(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, help_text="Optional title for the URL")
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=50, unique=True, default=generate_short_code, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
