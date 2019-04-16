from django.contrib import admin
from .models import *

@admin.register(Events)    
class EventAdmin(admin.ModelAdmin):
    pass