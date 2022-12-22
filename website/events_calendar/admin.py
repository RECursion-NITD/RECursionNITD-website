from django.contrib import admin
from .models import *


@admin.register(Events_Calendar)
class EventsCalenderAdmin(admin.ModelAdmin):
    search_fields = ('title', 'venue')
    list_filter = ('event_type', 'target_year',)
    list_display = ('__str__', 'event_type', 'target_year', 'venue')
