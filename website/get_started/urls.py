from django.urls import path
from .views import *
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

app_name = "get_started"
urlpatterns = [
    path('get_started/', get_started, name='get_started'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
