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
    # API endpoints for React frontend
    path('api/team/', team_api, name='team_api'),
    path('api/alumni/', alumni_api, name='alumni_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
