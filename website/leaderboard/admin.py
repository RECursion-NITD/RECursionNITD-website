from django.contrib import admin
from .models import CPProfile


@admin.register(CPProfile)
class CPProfileAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'codeforces_handle',
        'codeforces_rating',
        'codechef_handle',
        'codechef_rating',
        'batch',
        'dept',
        'last_synced',
    )
    search_fields = ('name', 'codeforces_handle', 'codechef_handle', 'username')
    list_filter = ('batch', 'dept', 'is_active')
    ordering = ('-codeforces_rating', '-codechef_rating')
