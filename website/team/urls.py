from django.urls import path
from .views import *
from django.conf.urls import include
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static

app_name="team"
urlpatterns = [
    path('team_page/', team_page, name='team_page'),
    path('alumni/', alumni_page, name='alumni'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
