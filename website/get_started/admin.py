from django.contrib import admin
from .models import *

get_started_models = [Level, Topic, Link, Note, File]
admin.site.register(get_started_models)
