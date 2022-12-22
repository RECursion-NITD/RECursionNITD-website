from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Experiences)
class ExperiencesAdmin(admin.ModelAdmin):
    search_fields = ('interview_Questions',)
    list_filter = ('role_Type', 'verification_Status', 'year', 'company')
    list_editable = ('verification_Status',)
    list_display = ('__str__', 'role_Type', 'company', 'verification_Status')


@admin.register(Revisions)
class RevisionsAdmin(admin.ModelAdmin):
    search_fields = ('experience',)
    list_display = ('__str__', 'message', 'experience')
