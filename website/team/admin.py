from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    pass