from django.contrib import admin
from .models import ShortenedUrl

@admin.register(ShortenedUrl)
class ShortenedUrlAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_code', 'original_url', 'click_count', 'created_at')
    search_fields = ('title', 'short_code', 'original_url')
    readonly_fields = ('click_count', 'created_at')
