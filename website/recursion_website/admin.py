from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Comments)
admin.site.register(Events)
admin.site.register(Follows)
admin.site.register(Taggings)

