from django.contrib import admin
from .models import *

getting_started_models = [Level,Topic,SubTopic,Note,File,Link,]
admin.site.register(getting_started_models)
