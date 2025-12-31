from django.urls import path
from .views import *
from django.conf.urls import include
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static

app_name = "events_calendar"
urlpatterns = [
                  path('', list_events, name='list_events'),
                  path('create/', create_event, name='create_event'),
                  path('detail/<int:event_id>/', event_detail, name='event_detail'),
                  path('update/<int:event_id>/', event_update, name='event_update'),
                  path('filter/<str:type>', filter_event, name='filter_event'),
                  url(r'^markdownx/', include('markdownx.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
