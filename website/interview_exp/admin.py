from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Experiences)
class ExperiencesAdmin(admin.ModelAdmin):
    pass

@admin.register(Revisions)
class RevisionsAdmin(admin.ModelAdmin):
    pass