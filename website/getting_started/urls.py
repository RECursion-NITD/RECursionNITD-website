from django.urls import path
from .views import * 
from django.conf.urls import include
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static

app_name = "getting_started"
urlpatterns = [
    path('', getting_started, name='getting_started'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)