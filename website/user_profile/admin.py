from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('name', 'user__email', 'user__username')
    list_filter = ('role',)
