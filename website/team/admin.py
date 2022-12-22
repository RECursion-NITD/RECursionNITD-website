from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('batch_year',)
    list_editable = ('designation',)
    list_display = ('__str__', 'designation', 'branch')
